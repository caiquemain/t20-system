import React, { useState, useMemo } from 'react';

interface Item {
    nome: string;
    qtd: number;
    espaco: number;
    descricao?: string;
    tipo: string;
    equipado: boolean;
}

interface EquipamentoCardProps {
    inventario: any;
    dadosEquipamentos: any;
    onUpdateInventario: (novoInventario: any) => void;
}

const ICONE_GERAL: Record<string, string> = { Aventura: '🎒', Alquímico: '⚗️', Símbolo: '✨', Ferramenta: '🛠️' };

export const EquipamentoCard: React.FC<EquipamentoCardProps> = ({
    inventario,
    dadosEquipamentos,
    onUpdateInventario,
}) => {
    const [modalAberto, setModalAberto] = useState(false);
    const [busca, setBusca] = useState('');
    const [filtroCategoria, setFiltroCategoria] = useState('todas');
    const [filtroProposito, setFiltroProposito] = useState('todos');
    const [filtroTipo, setFiltroTipo] = useState('todos');
    const [filtroGeral, setFiltroGeral] = useState('todos');
    const [tt, setTt] = useState<any>(null);

    const { equipamentos = [], carga_total = 0, carga_maxima = 0, sobrecargado = false, dinheiro } = inventario || {};
    const armas = dadosEquipamentos?.armas || {};
    const armaduras = dadosEquipamentos?.armaduras || {};
    const gerais = dadosEquipamentos?.gerais || {};

    // Limites T20 (p.141)
    const empunhados = equipamentos.filter((i: Item) => {
        const cat = armas[i.nome] || armaduras[i.nome];
        return i.equipado && cat?.proposito;
    }).length;
    const armadurasVestidas = equipamentos.filter((i: Item) => {
        const cat = armaduras[i.nome];
        return i.equipado && cat && cat.tipo_armadura !== 'Escudo';
    }).length;
    const escudosEmpunhados = equipamentos.filter((i: Item) => {
        const cat = armaduras[i.nome];
        return i.equipado && cat?.tipo_armadura === 'Escudo';
    }).length;

    const corCarga = sobrecargado ? '#ff5252' : carga_total > carga_maxima * 0.8 ? '#ffa726' : '#66bb6a';
    const percentual = carga_maxima > 0 ? Math.min(100, (carga_total / carga_maxima) * 100) : 0;

    // Filtros mutuamente excludentes (armas x armaduras x gerais)
    const modoArmadura = filtroTipo !== 'todos';
    const modoArma = filtroCategoria !== 'todas' || filtroProposito !== 'todos';
    const modoGeral = filtroGeral !== 'todos';

    const catalogoItens = useMemo(() => {
        const itens: any[] = [];
        const termo = busca.trim().toLowerCase();
        if (!modoGeral) {
            if (!modoArmadura) {
                Object.entries(armas).forEach(([nome, d]: [string, any]) => {
                    if (filtroCategoria !== 'todas' && d.categoria !== filtroCategoria) return;
                    if (filtroProposito !== 'todos' && d.proposito !== filtroProposito) return;
                    if (termo && !nome.toLowerCase().includes(termo)) return;
                    itens.push({ nome, d, tipoCat: 'arma' });
                });
            }
            if (!modoArma) {
                Object.entries(armaduras).forEach(([nome, d]: [string, any]) => {
                    if (filtroTipo !== 'todos' && d.tipo_armadura !== filtroTipo) return;
                    if (termo && !nome.toLowerCase().includes(termo)) return;
                    itens.push({ nome, d, tipoCat: 'armadura' });
                });
            }
        }
        if (!modoArma && !modoArmadura) {
            Object.entries(gerais).forEach(([nome, d]: [string, any]) => {
                if (modoGeral && d.subcategoria !== filtroGeral) return;
                if (termo && !nome.toLowerCase().includes(termo)) return;
                itens.push({ nome, d, tipoCat: 'geral' });
            });
        }
        return itens;
    }, [armas, armaduras, gerais, filtroCategoria, filtroProposito, filtroTipo, filtroGeral, busca, modoArmadura, modoArma, modoGeral]);

    const adicionarItem = (nome: string, tipoCat: string) => {
        const cat = armas[nome] || armaduras[nome] || gerais[nome];
        if (!cat) return;
        const novoItem: Item = {
            nome,
            qtd: 1,
            espaco: cat.espacos || 1,
            descricao: '',
            tipo: tipoCat === 'arma' ? 'Arma' : tipoCat === 'armadura' ? 'Armadura' : 'Geral',
            equipado: false,
        };
        onUpdateInventario({ ...inventario, equipamentos: [...equipamentos, novoItem] });
        setModalAberto(false);
    };

    const toggleEquipado = (index: number) => {
        const novos = [...equipamentos];
        const item = { ...novos[index] };
        if (gerais[item.nome]) return; // item geral não é equipável
        const cat = armas[item.nome] || armaduras[item.nome];
        if (!cat) return;
        if (!item.equipado) {
            if (cat.proposito && empunhados >= 2) { alert('Limite de 2 itens empunhados (1 por mão).'); return; }
            if (cat.tipo_armadura && cat.tipo_armadura !== 'Escudo' && armadurasVestidas >= 1) { alert('Limite de 1 armadura vestida.'); return; }
            if (cat.tipo_armadura === 'Escudo' && escudosEmpunhados >= 1) { alert('Limite de 1 escudo empunhado.'); return; }
        }
        item.equipado = !item.equipado;
        novos[index] = item;
        onUpdateInventario({ ...inventario, equipamentos: novos });
    };

    const removerItem = (index: number) => {
        onUpdateInventario({ ...inventario, equipamentos: equipamentos.filter((_: any, i: number) => i !== index) });
    };

    const alterarQuantidade = (index: number, delta: number) => {
        const novos = [...equipamentos];
        const item = { ...novos[index] };
        item.qtd = Math.max(1, item.qtd + delta);
        novos[index] = item;
        onUpdateInventario({ ...inventario, equipamentos: novos });
    };

    const getBadgeEstado = (item: Item) => {
        const cat = armas[item.nome] || armaduras[item.nome];
        if (gerais[item.nome] || !item.equipado) return { label: 'Guardado', cor: '#666' };
        if (cat?.proposito) return { label: 'Empunhada', cor: '#ff9800' };
        if (cat?.tipo_armadura === 'Escudo') return { label: 'Empunhado', cor: '#ff9800' };
        if (cat?.tipo_armadura) return { label: 'Vestida', cor: '#4caf50' };
        return { label: 'Equipado', cor: '#2196f3' };
    };

    const mostrarTooltip = (e: React.MouseEvent<HTMLDivElement>, conteudo: React.ReactNode) => {
        const r = e.currentTarget.getBoundingClientRect();
        const abaixo = r.top < 340;
        setTt({
            conteudo,
            x: Math.min(Math.max(r.left + r.width / 2, 130), window.innerWidth - 130),
            top: abaixo ? r.bottom + 8 : r.top - 8,
            abaixo,
        });
    };
    const esconderTooltip = () => setTt(null);

    // Tooltips padrão-ouro (mesmo design de perícias/status)
    const tooltipArma = (d: any) => (
        <div className="equip-tooltip-box">
            <div className="tooltip-row"><span>Preço</span><span>T$ {d.preco}</span></div>
            {d.dano && <div className="tooltip-row"><span>Dano</span><span>{d.dano} {d.tipo}</span></div>}
            <div className="tooltip-row"><span>Crítico</span><span>{d.critico}</span></div>
            <div className="tooltip-row"><span>Alcance</span><span>{d.alcance || '—'}</span></div>
            <div className="tooltip-row"><span>Empunhadura</span><span>{d.empunhadura}</span></div>
            <div className="tooltip-row"><span>Espaços</span><span>{d.espacos}</span></div>
            {(d.habilidades || []).map((h: string) => (
                <div key={h} className="tooltip-row source-row">
                    <span>↳ {h.charAt(0).toUpperCase() + h.slice(1)}</span>
                    <span>{h === 'versátil' && d.versatil ? d.versatil : '✓'}</span>
                </div>
            ))}
            {d.arremessavel && <div className="tooltip-row source-row"><span>↳ Arremessável</span><span>✓</span></div>}
            <div className="tooltip-total"><span>{d.categoria}</span><span>{d.proposito}</span></div>
        </div>
    );

    const tooltipArmadura = (d: any) => (
        <div className="equip-tooltip-box">
            <div className="tooltip-row"><span>Preço</span><span>T$ {d.preco}</span></div>
            <div className="tooltip-row"><span>Bônus Defesa</span><span>+{d.bonus_defesa}</span></div>
            <div className="tooltip-row"><span>Penalidade</span><span>{d.penalidade_armadura}</span></div>
            <div className="tooltip-row"><span>Espaços</span><span>{d.espacos}</span></div>
            {d.tipo_armadura === 'Pesada' && (
                <>
                    <div className="tooltip-row source-row"><span>↳ Sem DES na Defesa</span><span>✗</span></div>
                    <div className="tooltip-row source-row"><span>↳ Deslocamento</span><span>−3m</span></div>
                </>
            )}
            {d.extras && <div className="tooltip-row source-row"><span>↳ {d.extras}</span><span>✓</span></div>}
            <div className="tooltip-total"><span>{d.tipo_armadura === 'Escudo' ? 'Escudo' : 'Armadura'}</span><span>{d.tipo_armadura}</span></div>
        </div>
    );

    const tooltipGeral = (d: any) => (
        <div className="equip-tooltip-box">
            <div className="tooltip-row"><span>Preço</span><span>T$ {d.preco}</span></div>
            <div className="tooltip-row"><span>Espaços</span><span>{d.espacos}</span></div>
            {d.notas && <div className="tooltip-row source-row"><span>↳ {d.notas}</span><span>•</span></div>}
            <div className="tooltip-total"><span>Item Geral</span><span>{d.subcategoria}</span></div>
        </div>
    );

    const tooltipDe = (tipoCat: string, d: any) =>
        tipoCat === 'arma' ? tooltipArma(d) : tipoCat === 'armadura' ? tooltipArmadura(d) : tooltipGeral(d);

    const iconeDe = (tipoCat: string, d: any) =>
        tipoCat === 'arma' ? '⚔️' : tipoCat === 'armadura' ? '🛡️' : (ICONE_GERAL[d.subcategoria] || '🎒');

    const selectStyle = { padding: '6px 10px', borderRadius: 4, background: '#333', color: 'white', border: '1px solid #444', fontSize: '0.8rem' };
    const limpaConflitantes = (qual: 'arma' | 'armadura' | 'geral') => {
        if (qual !== 'arma') { setFiltroCategoria('todas'); setFiltroProposito('todos'); }
        if (qual !== 'armadura') setFiltroTipo('todos');
        if (qual !== 'geral') setFiltroGeral('todos');
    };

    return (
        <>
            <style>{`
                .equip-tooltip-box {
                    width: 240px; background-color: #1a1a1a;
                    border: 1px solid #ffd700; border-radius: 6px;
                    padding: 10px; box-shadow: 0 5px 20px rgba(0, 0, 0, 0.9);
                }
                .equip-tooltip-box .source-row {
                    font-size: 0.7rem; color: #888;
                    border-bottom: none; margin-bottom: 1px; padding-left: 5px;
                }
            `}</style>

            <div className="section-card" style={{ marginBottom: 20 }}>
                <h3 className="section-title" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    🎒 Equipamento
                    <button className="btn-action" onClick={() => setModalAberto(true)} style={{ padding: '6px 12px', fontSize: '0.85rem' }}>
                        + Adicionar Item
                    </button>
                </h3>

                <div style={{ marginBottom: 15 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 5 }}>
                        <span style={{ fontSize: '0.9rem', fontWeight: 'bold' }}>CARGA: {carga_total} / {carga_maxima}</span>
                        {sobrecargado && (
                            <span style={{ background: '#ff5252', color: 'white', padding: '2px 8px', borderRadius: 4, fontSize: '0.75rem', fontWeight: 'bold' }}>
                                SOBRECARGADO
                            </span>
                        )}
                    </div>
                    <div style={{ width: '100%', height: 8, background: '#1a1a1a', borderRadius: 4, overflow: 'hidden' }}>
                        <div style={{ width: `${percentual}%`, height: '100%', background: corCarga, transition: 'all 0.3s' }} />
                    </div>
                </div>

                {dinheiro && ((dinheiro.to ?? 0) > 0 || (dinheiro.tl ?? 0) > 0 || (dinheiro.tp ?? 0) > 0) && (
                    <div style={{ background: 'rgba(0,0,0,0.3)', padding: '8px 12px', borderRadius: 4, marginBottom: 15, display: 'flex', gap: 15, fontSize: '0.85rem' }}>
                        {(dinheiro.to ?? 0) > 0 && <span style={{ color: '#ffd700' }}>🪙 {dinheiro.to} TO</span>}
                        {(dinheiro.tl ?? 0) > 0 && <span style={{ color: '#c0c0c0' }}>🪙 {dinheiro.tl} T$</span>}
                        {(dinheiro.tp ?? 0) > 0 && <span style={{ color: '#cd7f32' }}>🪙 {dinheiro.tp} TC</span>}
                    </div>
                )}

                <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                    {equipamentos.length === 0 ? (
                        <p style={{ color: '#666', textAlign: 'center', padding: 20, margin: 0 }}>Nenhum item no inventário</p>
                    ) : (
                        equipamentos.map((item: Item, i: number) => {
                            const cat = armas[item.nome] || armaduras[item.nome] || gerais[item.nome];
                            const ehGeral = !!gerais[item.nome];
                            const badge = getBadgeEstado(item);
                            const icon = ehGeral
                                ? (ICONE_GERAL[cat?.subcategoria] || '🎒')
                                : (armas[item.nome] ? '⚔️' : '🛡️');
                            return (
                                <div key={i} style={{ background: 'rgba(0,0,0,0.3)', padding: 10, borderRadius: 4, display: 'flex', alignItems: 'center', gap: 10 }}>
                                    <span style={{ fontSize: '1.2rem' }}>{icon}</span>
                                    <div style={{ flex: 1 }}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                            <strong style={{ fontSize: '0.95rem' }}>{item.nome}</strong>
                                            <span style={{ fontSize: '0.7rem', padding: '2px 6px', borderRadius: 3, background: badge.cor, color: 'white' }}>{badge.label}</span>
                                        </div>
                                        {cat && (
                                            <div style={{ fontSize: '0.75rem', color: '#888', marginTop: 2 }}>
                                                {cat.dano && <span>{cat.dano} {cat.tipo} · </span>}
                                                {cat.bonus_defesa && <span>+{cat.bonus_defesa} Def · </span>}
                                                {ehGeral && cat.notas && <span>{cat.notas} · </span>}
                                                {cat.espacos || item.espaco} espaço(s)
                                            </div>
                                        )}
                                    </div>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                                        <button onClick={() => alterarQuantidade(i, -1)} style={{ background: '#333', border: 'none', color: 'white', width: 20, height: 20, borderRadius: 3, cursor: 'pointer' }}>−</button>
                                        <span style={{ fontSize: '0.9rem', minWidth: 20, textAlign: 'center' }}>{item.qtd}</span>
                                        <button onClick={() => alterarQuantidade(i, 1)} style={{ background: '#333', border: 'none', color: 'white', width: 20, height: 20, borderRadius: 3, cursor: 'pointer' }}>+</button>
                                    </div>
                                    {!ehGeral && (
                                        <button onClick={() => toggleEquipado(i)} style={{ background: item.equipado ? '#ff9800' : '#4caf50', border: 'none', color: 'white', padding: '4px 10px', borderRadius: 3, cursor: 'pointer', fontSize: '0.8rem' }}>
                                            {item.equipado ? 'Guardar' : 'Equipar'}
                                        </button>
                                    )}
                                    <button onClick={() => removerItem(i)} style={{ background: '#ff5252', border: 'none', color: 'white', width: 24, height: 24, borderRadius: 3, cursor: 'pointer' }}>🗑️</button>
                                </div>
                            );
                        })
                    )}
                </div>
            </div>

            {modalAberto && (
                <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.8)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999 }} onClick={() => setModalAberto(false)}>
                    <div style={{ background: '#1e1e1e', borderRadius: 8, padding: 20, maxWidth: '90%', maxHeight: '90vh', width: '850px', display: 'flex', flexDirection: 'column', border: '1px solid #ffd700' }} onClick={(e) => e.stopPropagation()}>
                        <h2 style={{ margin: '0 0 15px 0' }}>🎒 Adicionar Item</h2>

                        <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginBottom: 15 }}>
                            <input value={busca} onChange={(e) => setBusca(e.target.value)} placeholder="🔍 Buscar item..." className="input-dark" style={{ flex: 1, minWidth: 180 }} />
                            <select value={filtroCategoria} onChange={(e) => { setFiltroCategoria(e.target.value); if (e.target.value !== 'todas') limpaConflitantes('arma'); }} style={selectStyle}>
                                <option value="todas">Armas: todas</option>
                                <option value="Simples">Simples</option>
                                <option value="Marcial">Marcial</option>
                                <option value="Exótica">Exótica</option>
                                <option value="Fogo">De Fogo</option>
                            </select>
                            <select value={filtroProposito} onChange={(e) => { setFiltroProposito(e.target.value); if (e.target.value !== 'todos') limpaConflitantes('arma'); }} style={selectStyle}>
                                <option value="todos">Propósito: todos</option>
                                <option value="Corpo a Corpo">Corpo a Corpo</option>
                                <option value="À Distância">À Distância</option>
                            </select>
                            <select value={filtroTipo} onChange={(e) => { setFiltroTipo(e.target.value); if (e.target.value !== 'todos') limpaConflitantes('armadura'); }} style={selectStyle}>
                                <option value="todos">Armaduras: todas</option>
                                <option value="Leve">Armadura Leve</option>
                                <option value="Pesada">Armadura Pesada</option>
                                <option value="Escudo">Escudo</option>
                            </select>
                            <select value={filtroGeral} onChange={(e) => { setFiltroGeral(e.target.value); if (e.target.value !== 'todos') limpaConflitantes('geral'); }} style={selectStyle}>
                                <option value="todos">Gerais: todos</option>
                                <option value="Aventura">Aventura</option>
                                <option value="Alquímico">Alquímico</option>
                                <option value="Símbolo">Símbolo</option>
                                <option value="Ferramenta">Ferramenta</option>
                            </select>
                        </div>

                        <div style={{ flex: 1, overflowY: 'auto', marginBottom: 15, paddingTop: 4 }} onScroll={() => setTt(null)}>
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: 12, rowGap: 16 }}>
                                {catalogoItens.map(({ nome, d, tipoCat }) => (
                                    <div key={nome}
                                        onClick={() => adicionarItem(nome, tipoCat)}
                                        style={{ background: '#252525', padding: 12, borderRadius: 6, cursor: 'pointer', border: '2px solid #333', transition: 'all 0.2s' }}
                                        onMouseEnter={(e) => { e.currentTarget.style.borderColor = '#ffd700'; mostrarTooltip(e, tooltipDe(tipoCat, d)); }}
                                        onMouseLeave={(e) => { e.currentTarget.style.borderColor = '#333'; esconderTooltip(); }}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
                                            <span style={{ fontSize: '1.2rem' }}>{iconeDe(tipoCat, d)}</span>
                                            <strong style={{ fontSize: '0.9rem' }}>{nome}</strong>
                                        </div>
                                        <div style={{ fontSize: '0.8rem', color: '#80deea', marginBottom: 4 }}>
                                            {tipoCat === 'arma' ? (d.dano ? `${d.dano} ${d.tipo || ''}` : 'Sem dano')
                                                : tipoCat === 'armadura' ? `+${d.bonus_defesa} Defesa`
                                                : (d.notas || d.subcategoria)}
                                        </div>
                                        <div style={{ fontSize: '0.75rem', color: '#888' }}>
                                            {tipoCat === 'arma' ? `${d.categoria} · ${d.empunhadura} · ${d.espacos} esp`
                                                : tipoCat === 'armadura' ? `${d.tipo_armadura} · ${d.espacos} esp`
                                                : `${d.subcategoria} · ${d.espacos} esp`}
                                        </div>
                                    </div>
                                ))}
                                {catalogoItens.length === 0 && (
                                    <p style={{ color: '#666', gridColumn: '1 / -1', textAlign: 'center' }}>Nenhum item com esses filtros</p>
                                )}
                            </div>
                        </div>

                        <button onClick={() => setModalAberto(false)} style={{ background: '#ff5252', border: 'none', color: 'white', padding: '8px 16px', borderRadius: 4, cursor: 'pointer', fontSize: '0.9rem', alignSelf: 'flex-end' }}>
                            Fechar
                        </button>
                    </div>
                </div>
            )}

            {tt && (
                <div style={{
                    position: 'fixed',
                    left: tt.x,
                    top: tt.top,
                    transform: tt.abaixo ? 'translateX(-50%)' : 'translate(-50%, -100%)',
                    zIndex: 10000,
                    pointerEvents: 'none',
                }}>
                    {tt.conteudo}
                </div>
            )}
        </>
    );
};
