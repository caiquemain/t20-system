import React, { useEffect, useState } from 'react';
import {
    criarAmeaca,
    fetchTabelasConstrutorAmeacas,
    gerarAmeacaManual,
} from '../services/api';
import type { Ameaca } from '../types';

interface Props {
    onClose: () => void;
    onCreated: (ameaca: Ameaca) => void;
}

interface LinhaTabela {
    patamar: string;
    ataque: number;
    dano_medio: number;
    defesa: number;
    res_forte: number;
    res_media: number;
    res_fraca: number;
    pv: number;
    cd: number;
}

interface TabelasData {
    nds: string[];
    tipos: string[];
    tamanhos: string[];
    tesouros: string[];
    deslocamento_por_tamanho: Record<string, string>;
    tabelas: Record<string, Record<string, LinhaTabela>>;
}

interface AtaqueForm {
    nome: string;
    tipo: 'corpo_a_corpo' | 'distancia';
    bonus: number;
    dano: string;
}

interface HabForm {
    nome: string;
    descricao: string;
    custo_pm: string;
    magica: boolean;
}

const RESISTENCIAS = [
    { id: 'fortitude', label: 'Fortitude' },
    { id: 'reflexos', label: 'Reflexos' },
    { id: 'vontade', label: 'Vontade' },
] as const;

export const ConstrutorAmeacaModal: React.FC<Props> = ({ onClose, onCreated }) => {
    const [tabelas, setTabelas] = useState<TabelasData | null>(null);
    const [salvando, setSalvando] = useState(false);
    const [erro, setErro] = useState('');

    // Passo 0-2: Conceito, Tipo, Tamanho, Papel e ND
    const [nome, setNome] = useState('');
    const [tipo, setTipo] = useState('Monstro');
    const [tamanho, setTamanho] = useState('Médio');
    const [papel, setPapel] = useState<'solo' | 'lacaio' | 'especial'>('solo');
    const [nd, setNd] = useState('1');
    const [deslocamento, setDeslocamento] = useState('9m (6q)');

    // Passo 3: Distribuição de resistências e ajustes finos
    const [resForte, setResForte] = useState('fortitude');
    const [resMedia, setResMedia] = useState('reflexos');
    const [resFraca, setResFraca] = useState('vontade');
    const [ajusteDefesa, setAjusteDefesa] = useState(0);
    const [ajustePv, setAjustePv] = useState(0);
    const [ajusteAtaque, setAjusteAtaque] = useState(0);
    const [ajusteCd, setAjusteCd] = useState(0);
    const [pmManual, setPmManual] = useState('');

    // Passo 4-5: Ataques e Habilidades
    const [ataques, setAtaques] = useState<AtaqueForm[]>([
        { nome: 'Garra / Espada', tipo: 'corpo_a_corpo', bonus: 9, dano: '2d8+6' },
    ]);
    const [habilidades, setHabilidades] = useState<HabForm[]>([]);

    // Passo 6-7: Atributos, Sentidos, Equipamento e Tesouro
    const [atributos, setAtributos] = useState({
        forca: 2,
        destreza: 1,
        constituicao: 2,
        inteligencia: 0,
        sabedoria: 1,
        carisma: 0,
    });
    const [sentidosStr, setSentidosStr] = useState('Visão no escuro');
    const [equipamento, setEquipamento] = useState('');
    const [tesouro, setTesouro] = useState('Padrão');

    useEffect(() => {
        fetchTabelasConstrutorAmeacas()
            .then(res => setTabelas(res.data))
            .catch(() => setErro('Não foi possível carregar as tabelas do Manual de Criação de Ameaças.'));
    }, []);

    const linhaAtual: LinhaTabela | null = tabelas?.tabelas?.[papel]?.[nd] || null;

    // Atualiza bônus do 1º ataque quando muda Papel/ND/ajusteAtaque
    useEffect(() => {
        if (!linhaAtual) return;
        setAtaques(prev => {
            if (prev.length === 0) return prev;
            const first = { ...prev[0], bonus: linhaAtual.ataque + ajusteAtaque };
            return [first, ...prev.slice(1)];
        });
    }, [linhaAtual?.ataque, ajusteAtaque]);

    useEffect(() => {
        if (tabelas?.deslocamento_por_tamanho?.[tamanho]) {
            setDeslocamento(tabelas.deslocamento_por_tamanho[tamanho]);
        }
    }, [tamanho, tabelas]);

    const patamarIndice = (p?: string) => {
        if (p === 'Veterano') return 2;
        if (p === 'Campeão') return 3;
        if (p === 'Lenda' || p === 'L+') return 4;
        return 1;
    };

    const habsSugeridas = () => {
        const idx = patamarIndice(linhaAtual?.patamar);
        return papel === 'especial' ? `${idx * 2} a ${idx * 3}` : `${idx} a ${idx * 2}`;
    };

    const handleSalvar = async () => {
        if (!nome.trim()) {
            setErro('Informe o nome da ameaça.');
            return;
        }
        setErro('');
        setSalvando(true);
        try {
            const payload = {
                nome: nome.trim(),
                nd,
                papel,
                tipo,
                tamanho,
                res_forte: resForte,
                res_media: resMedia,
                res_fraca: resFraca,
                deslocamento: deslocamento.trim() || '9m (6q)',
                pontos_de_mana: pmManual.trim() ? Number(pmManual) : null,
                sentidos: sentidosStr.split(',').map(s => s.trim()).filter(Boolean),
                ataques: ataques
                    .filter(a => a.nome.trim())
                    .map(a => ({
                        nome: a.nome.trim(),
                        modalidade: a.tipo === 'distancia' ? 'à distância' : 'corpo a corpo',
                        bonus_ataque: Number(a.bonus) || 0,
                        dano: a.dano.trim() || '1d8+2',
                    })),
                habilidades: habilidades
                    .filter(h => h.nome.trim())
                    .map(h => ({
                        nome: h.nome.trim(),
                        descricao: h.descricao.trim() || 'Habilidade especial.',
                        custo_pm: h.custo_pm.trim() ? Number(h.custo_pm) : null,
                        magica: h.magica,
                    })),
                atributos,
                equipamento: equipamento.trim() || null,
                tesouro,
                ajustes: {
                    defesa: ajusteDefesa,
                    pv: ajustePv,
                    ataque: ajusteAtaque,
                    cd: ajusteCd,
                },
            };

            const geradaRes = await gerarAmeacaManual(payload);
            const salvaRes = await criarAmeaca(geradaRes.data);
            onCreated(salvaRes.data);
        } catch (e: any) {
            setErro(e?.response?.data?.detail || 'Erro ao criar ameaça.');
        } finally {
            setSalvando(false);
        }
    };

    const inputStyle: React.CSSProperties = {
        width: '100%',
        padding: '8px 10px',
        background: '#222',
        border: '1px solid #444',
        borderRadius: 6,
        color: '#fff',
        boxSizing: 'border-box',
    };

    return (
        <div
            style={{
                position: 'fixed',
                inset: 0,
                background: 'rgba(0,0,0,0.82)',
                zIndex: 1000,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: 16,
            }}
        >
            <div
                style={{
                    width: '100%',
                    maxWidth: 920,
                    maxHeight: '90vh',
                    overflowY: 'auto',
                    background: '#161616',
                    border: '1px solid #d32f2f',
                    borderRadius: 10,
                    padding: 24,
                    color: '#eee',
                }}
            >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
                    <div>
                        <h2 style={{ margin: 0, color: '#ef5350' }}>Construtor de Ameaças (Manual Oficial)</h2>
                        <small style={{ color: '#999' }}>Ameaças de Arton — Tabelas 2-3 A/B/C (Solos, Lacaios e Especiais)</small>
                    </div>
                    <button
                        onClick={onClose}
                        style={{ background: '#333', color: '#fff', border: '1px solid #555', borderRadius: 6, padding: '6px 12px', cursor: 'pointer' }}
                    >
                        Fechar
                    </button>
                </div>

                {erro && (
                    <div style={{ background: 'rgba(211,47,47,0.2)', border: '1px solid #ef5350', padding: 10, borderRadius: 6, marginBottom: 14, color: '#ffcdd2' }}>
                        {erro}
                    </div>
                )}

                {/* PASSO 0-2 */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(170px, 1fr))', gap: 12, marginBottom: 16 }}>
                    <div style={{ gridColumn: 'span 2' }}>
                        <label style={{ fontSize: '0.8rem', color: '#bbb' }}>Nome da Ameaça *</label>
                        <input style={inputStyle} value={nome} onChange={e => setNome(e.target.value)} placeholder="Ex: Golem de Obsidiana" />
                    </div>
                    <div>
                        <label style={{ fontSize: '0.8rem', color: '#bbb' }}>Papel (Tabela 2-3)</label>
                        <select style={inputStyle} value={papel} onChange={e => setPapel(e.target.value as any)}>
                            <option value="solo">Solo (2-3 A)</option>
                            <option value="lacaio">Lacaio (2-3 B)</option>
                            <option value="especial">Especial (2-3 C)</option>
                        </select>
                    </div>
                    <div>
                        <label style={{ fontSize: '0.8rem', color: '#bbb' }}>ND</label>
                        <select style={inputStyle} value={nd} onChange={e => setNd(e.target.value)}>
                            {(tabelas?.nds || ['1/4', '1/2', '1', '2', '3', '4', '5', '10', '15', '20', 'S', 'S+']).map(n => (
                                <option key={n} value={n}>ND {n}</option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label style={{ fontSize: '0.8rem', color: '#bbb' }}>Tipo</label>
                        <select style={inputStyle} value={tipo} onChange={e => setTipo(e.target.value)}>
                            {(tabelas?.tipos || ['Animal', 'Construto', 'Espírito', 'Humanoide', 'Monstro', 'Morto-vivo']).map(t => (
                                <option key={t} value={t}>{t}</option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label style={{ fontSize: '0.8rem', color: '#bbb' }}>Tamanho</label>
                        <select style={inputStyle} value={tamanho} onChange={e => setTamanho(e.target.value)}>
                            {(tabelas?.tamanhos || ['Minúsculo', 'Pequeno', 'Médio', 'Grande', 'Enorme', 'Colossal']).map(t => (
                                <option key={t} value={t}>{t}</option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label style={{ fontSize: '0.8rem', color: '#bbb' }}>Deslocamento</label>
                        <input style={inputStyle} value={deslocamento} onChange={e => setDeslocamento(e.target.value)} />
                    </div>
                    <div>
                        <label style={{ fontSize: '0.8rem', color: '#bbb' }}>Tesouro</label>
                        <select style={inputStyle} value={tesouro} onChange={e => setTesouro(e.target.value)}>
                            {(tabelas?.tesouros || ['Nenhum', 'Metade', 'Padrão', 'Dobro']).map(t => (
                                <option key={t} value={t}>{t}</option>
                            ))}
                        </select>
                    </div>
                </div>

                {/* PREVIEW OFICIAL DA TABELA 2-3 */}
                {linhaAtual && (
                    <div style={{ background: '#211818', border: '1px solid #6d2626', borderRadius: 8, padding: 14, marginBottom: 16 }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: 8, marginBottom: 10 }}>
                            <strong style={{ color: '#ffb74d' }}>
                                Parâmetros Oficiais — {papel.toUpperCase()} ND {nd} ({linhaAtual.patamar})
                            </strong>
                            <span style={{ fontSize: '0.82rem', color: '#bbb' }}>
                                Habilidades sugeridas: <strong>{habsSugeridas()}</strong>
                            </span>
                        </div>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(110px, 1fr))', gap: 8, textAlign: 'center' }}>
                            <div style={{ background: '#181818', padding: 8, borderRadius: 6 }}>
                                <div style={{ fontSize: '0.72rem', color: '#aaa' }}>ATAQUE</div>
                                <div style={{ fontSize: '1.1rem', fontWeight: 'bold', color: '#ff8a65' }}>+{linhaAtual.ataque + ajusteAtaque}</div>
                            </div>
                            <div style={{ background: '#181818', padding: 8, borderRadius: 6 }}>
                                <div style={{ fontSize: '0.72rem', color: '#aaa' }}>DANO MÉDIO</div>
                                <div style={{ fontSize: '1.1rem', fontWeight: 'bold', color: '#ff8a65' }}>{linhaAtual.dano_medio}</div>
                            </div>
                            <div style={{ background: '#181818', padding: 8, borderRadius: 6 }}>
                                <div style={{ fontSize: '0.72rem', color: '#aaa' }}>DEFESA</div>
                                <div style={{ fontSize: '1.1rem', fontWeight: 'bold', color: '#64b5f6' }}>{linhaAtual.defesa + ajusteDefesa}</div>
                            </div>
                            <div style={{ background: '#181818', padding: 8, borderRadius: 6 }}>
                                <div style={{ fontSize: '0.72rem', color: '#aaa' }}>PV</div>
                                <div style={{ fontSize: '1.1rem', fontWeight: 'bold', color: '#81c784' }}>{linhaAtual.pv + ajustePv}</div>
                            </div>
                            <div style={{ background: '#181818', padding: 8, borderRadius: 6 }}>
                                <div style={{ fontSize: '0.72rem', color: '#aaa' }}>CD EFEITOS</div>
                                <div style={{ fontSize: '1.1rem', fontWeight: 'bold', color: '#ce93d8' }}>{linhaAtual.cd + ajusteCd}</div>
                            </div>
                            <div style={{ background: '#181818', padding: 8, borderRadius: 6 }}>
                                <div style={{ fontSize: '0.72rem', color: '#aaa' }}>RES (80/50/20%)</div>
                                <div style={{ fontSize: '0.95rem', fontWeight: 'bold', color: '#ffd54f' }}>
                                    +{linhaAtual.res_forte} / +{linhaAtual.res_media} / {linhaAtual.res_fraca >= 0 ? `+${linhaAtual.res_fraca}` : linhaAtual.res_fraca}
                                </div>
                            </div>
                        </div>

                        {/* Distribuição de Resistências + Ajustes Finos */}
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: 10, marginTop: 12 }}>
                            <div>
                                <label style={{ fontSize: '0.75rem', color: '#bbb' }}>Res. Forte (+{linhaAtual.res_forte})</label>
                                <select style={inputStyle} value={resForte} onChange={e => setResForte(e.target.value)}>
                                    {RESISTENCIAS.map(r => <option key={r.id} value={r.id}>{r.label}</option>)}
                                </select>
                            </div>
                            <div>
                                <label style={{ fontSize: '0.75rem', color: '#bbb' }}>Res. Média (+{linhaAtual.res_media})</label>
                                <select style={inputStyle} value={resMedia} onChange={e => setResMedia(e.target.value)}>
                                    {RESISTENCIAS.map(r => <option key={r.id} value={r.id}>{r.label}</option>)}
                                </select>
                            </div>
                            <div>
                                <label style={{ fontSize: '0.75rem', color: '#bbb' }}>Res. Fraca ({linhaAtual.res_fraca >= 0 ? `+${linhaAtual.res_fraca}` : linhaAtual.res_fraca})</label>
                                <select style={inputStyle} value={resFraca} onChange={e => setResFraca(e.target.value)}>
                                    {RESISTENCIAS.map(r => <option key={r.id} value={r.id}>{r.label}</option>)}
                                </select>
                            </div>
                            <div>
                                <label style={{ fontSize: '0.75rem', color: '#bbb' }}>PM (opcional)</label>
                                <input style={inputStyle} type="number" value={pmManual} onChange={e => setPmManual(e.target.value)} placeholder={papel === 'especial' ? 'Auto' : '0'} />
                            </div>
                        </div>

                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 8, marginTop: 10 }}>
                            <div>
                                <label style={{ fontSize: '0.72rem', color: '#999' }}>Ajuste Defesa</label>
                                <input style={inputStyle} type="number" value={ajusteDefesa} onChange={e => setAjusteDefesa(Number(e.target.value))} />
                            </div>
                            <div>
                                <label style={{ fontSize: '0.72rem', color: '#999' }}>Ajuste PV</label>
                                <input style={inputStyle} type="number" value={ajustePv} onChange={e => setAjustePv(Number(e.target.value))} />
                            </div>
                            <div>
                                <label style={{ fontSize: '0.72rem', color: '#999' }}>Ajuste Ataque</label>
                                <input style={inputStyle} type="number" value={ajusteAtaque} onChange={e => setAjusteAtaque(Number(e.target.value))} />
                            </div>
                            <div>
                                <label style={{ fontSize: '0.72rem', color: '#999' }}>Ajuste CD</label>
                                <input style={inputStyle} type="number" value={ajusteCd} onChange={e => setAjusteCd(Number(e.target.value))} />
                            </div>
                        </div>
                    </div>
                )}

                {/* ATAQUES */}
                <div style={{ marginBottom: 16 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                        <strong style={{ color: '#ff8a65' }}>Ataques</strong>
                        <button
                            type="button"
                            onClick={() => setAtaques([...ataques, { nome: 'Mordida', tipo: 'corpo_a_corpo', bonus: (linhaAtual?.ataque || 6) + ajusteAtaque, dano: '1d8+4' }])}
                            style={{ background: '#333', color: '#fff', border: '1px solid #555', borderRadius: 6, padding: '4px 10px', cursor: 'pointer', fontSize: '0.8rem' }}
                        >
                            + Ataque
                        </button>
                    </div>
                    {ataques.map((a, idx) => (
                        <div key={idx} style={{ display: 'grid', gridTemplateColumns: '2fr 1.2fr 0.8fr 1.2fr auto', gap: 8, marginBottom: 6 }}>
                            <input style={inputStyle} value={a.nome} onChange={e => setAtaques(ataques.map((x, i) => i === idx ? { ...x, nome: e.target.value } : x))} placeholder="Nome do ataque" />
                            <select style={inputStyle} value={a.tipo} onChange={e => setAtaques(ataques.map((x, i) => i === idx ? { ...x, tipo: e.target.value as any } : x))}>
                                <option value="corpo_a_corpo">Corpo a Corpo</option>
                                <option value="distancia">À Distância</option>
                            </select>
                            <input style={inputStyle} type="number" value={a.bonus} onChange={e => setAtaques(ataques.map((x, i) => i === idx ? { ...x, bonus: Number(e.target.value) } : x))} placeholder="Bônus" />
                            <input style={inputStyle} value={a.dano} onChange={e => setAtaques(ataques.map((x, i) => i === idx ? { ...x, dano: e.target.value } : x))} placeholder="Ex: 2d8+8" />
                            <button type="button" onClick={() => setAtaques(ataques.filter((_, i) => i !== idx))} style={{ background: '#4a1c1c', color: '#fff', border: 'none', borderRadius: 6, padding: '0 10px', cursor: 'pointer' }}>×</button>
                        </div>
                    ))}
                </div>

                {/* HABILIDADES */}
                <div style={{ marginBottom: 16 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                        <strong style={{ color: '#ce93d8' }}>Habilidades ({habilidades.length})</strong>
                        <button
                            type="button"
                            onClick={() => setHabilidades([...habilidades, { nome: '', descricao: '', custo_pm: '', magica: false }])}
                            style={{ background: '#333', color: '#fff', border: '1px solid #555', borderRadius: 6, padding: '4px 10px', cursor: 'pointer', fontSize: '0.8rem' }}
                        >
                            + Habilidade
                        </button>
                    </div>
                    {habilidades.map((h, idx) => (
                        <div key={idx} style={{ background: '#1e1e1e', padding: 10, borderRadius: 6, marginBottom: 8, border: '1px solid #333' }}>
                            <div style={{ display: 'grid', gridTemplateColumns: '2fr 0.7fr auto auto', gap: 8, marginBottom: 6, alignItems: 'center' }}>
                                <input style={inputStyle} value={h.nome} onChange={e => setHabilidades(habilidades.map((x, i) => i === idx ? { ...x, nome: e.target.value } : x))} placeholder="Nome da habilidade" />
                                <input style={inputStyle} type="number" value={h.custo_pm} onChange={e => setHabilidades(habilidades.map((x, i) => i === idx ? { ...x, custo_pm: e.target.value } : x))} placeholder="PM" />
                                <label style={{ fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: 4 }}>
                                    <input type="checkbox" checked={h.magica} onChange={e => setHabilidades(habilidades.map((x, i) => i === idx ? { ...x, magica: e.target.checked } : x))} />
                                    Mágica
                                </label>
                                <button type="button" onClick={() => setHabilidades(habilidades.filter((_, i) => i !== idx))} style={{ background: '#4a1c1c', color: '#fff', border: 'none', borderRadius: 6, padding: '6px 10px', cursor: 'pointer' }}>×</button>
                            </div>
                            <textarea style={{ ...inputStyle, minHeight: 46 }} value={h.descricao} onChange={e => setHabilidades(habilidades.map((x, i) => i === idx ? { ...x, descricao: e.target.value } : x))} placeholder="Descrição mecânica da habilidade..." />
                        </div>
                    ))}
                </div>

                {/* ATRIBUTOS E EXTRAS */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: 8, marginBottom: 14 }}>
                    {(Object.keys(atributos) as Array<keyof typeof atributos>).map(k => (
                        <div key={k}>
                            <label style={{ fontSize: '0.72rem', color: '#aaa', textTransform: 'uppercase' }}>{k.slice(0, 3)}</label>
                            <input
                                style={inputStyle}
                                type="number"
                                value={atributos[k]}
                                onChange={e => setAtributos({ ...atributos, [k]: Number(e.target.value) })}
                            />
                        </div>
                    ))}
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 20 }}>
                    <div>
                        <label style={{ fontSize: '0.8rem', color: '#bbb' }}>Sentidos (separados por vírgula)</label>
                        <input style={inputStyle} value={sentidosStr} onChange={e => setSentidosStr(e.target.value)} placeholder="Visão no escuro, Faro" />
                    </div>
                    <div>
                        <label style={{ fontSize: '0.8rem', color: '#bbb' }}>Equipamento</label>
                        <input style={inputStyle} value={equipamento} onChange={e => setEquipamento(e.target.value)} placeholder="Ex: Espada longa, couraça..." />
                    </div>
                </div>

                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 10 }}>
                    <button onClick={onClose} style={{ background: '#333', color: '#fff', border: '1px solid #555', borderRadius: 6, padding: '10px 18px', cursor: 'pointer' }}>
                        Cancelar
                    </button>
                    <button
                        onClick={handleSalvar}
                        disabled={salvando}
                        style={{ background: '#d32f2f', color: '#fff', border: 'none', borderRadius: 6, padding: '10px 22px', fontWeight: 'bold', cursor: 'pointer' }}
                    >
                        {salvando ? 'Salvando...' : 'Salvar no Bestiário'}
                    </button>
                </div>
            </div>
        </div>
    );
};
