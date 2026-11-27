import { useMemo, useState } from 'react';
import type { WizardStepProps } from '../../../types/wizard';
import type { Habilidade } from '../../../types';
import { PowerSelectorModal } from '../../PowerSelectorModal';
import { T20Icon } from '../../T20Icon';

const FONT_BODY = "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif";

const ehPoderDeSlotClasse = (h: any): boolean => {
    const tipo = (h?.tipo || '').toString();
    const fonte = (h?.fonte || '').toString();
    if (fonte.startsWith('Origem:') || fonte.startsWith('Habilidade:') || fonte.startsWith('Devoção:')) {
        return false;
    }
    return tipo.includes('Poder de') || tipo.includes('Poder Geral') || tipo === 'Poder da Tormenta';
};

export function StepPoderes({
    ficha,
    updateFicha,
    dadosOrigens,
    dadosDeuses,
    dadosPoderesConcedidos,
    dadosHabilidadesClasse,
    dadosHabilidades,
    dadosHabilidadesRaciais,
    dadosMagias,
    listaPoderes,
    listaTodasPericias,
}: WizardStepProps) {
    const [slotEmEdicao, setSlotEmEdicao] = useState<number | null>(null);

    const origemNome = ficha.cabecalho.origem || '';
    const infoOrigem = dadosOrigens[origemNome];
    const beneficiosOrigem: string[] = useMemo(() => {
        if (!infoOrigem) return [];
        if (Array.isArray(infoOrigem.beneficios_lista)) {
            return infoOrigem.beneficios_lista;
        }
        return [
            ...(Array.isArray(infoOrigem.pericias) ? infoOrigem.pericias : []),
            ...(Array.isArray(infoOrigem.poderes) ? infoOrigem.poderes : []),
        ];
    }, [infoOrigem]);
    const escolhasOrigem = Array.isArray(ficha.escolhas_origem) ? ficha.escolhas_origem : [];

    const deusNome = ficha.cabecalho.deus || '';
    const infoDeus = dadosDeuses[deusNome];
    const poderesDeus: string[] = Array.isArray(infoDeus?.poderes) ? infoDeus.poderes : [];
    const poderConcedidoAtual = useMemo(
        () => (ficha.habilidades || []).find(h => (h.tipo || '').includes('Poder Concedido') || poderesDeus.includes(h.nome))?.nome || '',
        [ficha.habilidades, poderesDeus]
    );

    const classeNome = ficha.classes[0]?.nome || '';
    const nivel = Math.max(1, Number(ficha.classes[0]?.nivel || 1));
    const slotsPoderes = Math.max(0, nivel - 1);
    const poderesClasseAtuais = useMemo(
        () => (ficha.habilidades || []).filter(ehPoderDeSlotClasse).map(h => h.nome),
        [ficha.habilidades]
    );

    const poderesDisponiveisModal = useMemo(() => {
        const daClasse = Object.values(dadosHabilidadesClasse || {})
            .filter((h: any) => h.classe === classeNome && h.tipo && h.tipo.includes('Poder de'))
            .map((h: any) => ({
                nome: h.nome,
                tipo: h.tipo,
                categoria: h.classe,
                descricao: h.descricao,
                requisitos: h.requisitos || [],
            }));
        return [...daClasse, ...(listaPoderes || [])];
    }, [dadosHabilidadesClasse, classeNome, listaPoderes]);

    const handleToggleBeneficioOrigem = (beneficio: string) => {
        const jaTem = escolhasOrigem.includes(beneficio);
        let novas: string[];
        if (jaTem) {
            novas = escolhasOrigem.filter(b => b !== beneficio);
        } else {
            if (escolhasOrigem.length >= 2) return;
            novas = [...escolhasOrigem, beneficio];
        }
        updateFicha({ escolhas_origem: novas }, true);
    };

    const handleSelectPoderConcedido = (nomePoder: string) => {
        const dPoder = dadosPoderesConcedidos?.[nomePoder];
        const semAntigos = (ficha.habilidades || []).filter(h => !(h.tipo || '').includes('Poder Concedido'));
        if (poderConcedidoAtual === nomePoder) {
            updateFicha({ habilidades: semAntigos }, true);
            return;
        }
        const novo: Habilidade = {
            nome: dPoder?.nome || nomePoder,
            tipo: 'Poder Concedido',
            descricao: dPoder?.descricao || 'Poder concedido pela divindade.',
            fonte: `Devoção: ${deusNome}`,
            efeitos: dPoder?.efeitos || {},
        };
        updateFicha({ habilidades: [...semAntigos, novo] }, true);
    };

    const handleSelectPoderNivel = (valor: string) => {
        if (slotEmEdicao === null) return;
        const novosNomes = [...poderesClasseAtuais];
        while (novosNomes.length <= slotEmEdicao) novosNomes.push('');
        novosNomes[slotEmEdicao] = valor;

        const baseHabs = (ficha.habilidades || []).filter(h => !ehPoderDeSlotClasse(h));
        const novosPoderes: Habilidade[] = novosNomes.filter(Boolean).map(nome => {
            let d = Object.values(dadosHabilidadesClasse || {}).find((x: any) => x.nome === nome) as any;
            if (!d) d = Object.values(dadosHabilidades || {}).find((x: any) => x.nome === nome);
            return {
                nome,
                tipo: d?.tipo || 'Poder de Classe',
                descricao: d?.descricao || 'Poder selecionado',
                fonte: d?.classe || classeNome || 'Classe',
                efeitos: d?.efeitos || {},
                escolhas_aplicadas: {},
            };
        });
        updateFicha({ habilidades: [...baseHabs, ...novosPoderes] }, true);
        setSlotEmEdicao(null);
    };

    return (
        <div style={{ fontFamily: FONT_BODY, textTransform: 'none', display: 'flex', flexDirection: 'column', gap: 24 }}>
            <div>
                <h2 style={{ color: '#ffd700', marginBottom: 8, fontFamily: 'Tormenta, serif', display: 'inline-flex', alignItems: 'center', gap: 8 }}>
                    <T20Icon name="efeito" size={22} /> Passo 5: Origem, Devoção & Poderes
                </h2>
                <p style={{ color: '#94a3b8', margin: 0, fontSize: '0.92rem' }}>
                    Escolha os benefícios da sua origem, o poder concedido da sua divindade e os poderes de classe ou gerais ganhos por nível.
                </p>
            </div>

            {/* 1. Benefícios de Origem */}
            <div style={{ background: '#1a1d2e', border: '1px solid #32385a', borderRadius: 10, padding: 18 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
                    <h3 style={{ margin: 0, color: '#ffd700', fontSize: '1rem', fontFamily: 'Tormenta, serif' }}>
                        Benefícios de Origem {origemNome ? `(${origemNome})` : ''}
                    </h3>
                    {beneficiosOrigem.length > 0 && (
                        <span style={{ fontSize: '0.82rem', color: escolhasOrigem.length === 2 ? '#81c784' : '#ffb74d', fontWeight: 700 }}>
                            {escolhasOrigem.length} / 2 escolhidos
                        </span>
                    )}
                </div>
                {infoOrigem?.regional ? (
                    <div style={{
                        background: 'rgba(46, 125, 50, 0.14)',
                        border: '1px solid #2e7d32',
                        borderRadius: 8,
                        padding: '12px 14px',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: 6,
                    }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
                            <span style={{ color: '#81c784', fontWeight: 700, fontSize: '0.88rem' }}>
                                Benefício Único Regional (Automático)
                            </span>
                            {infoOrigem.regiao && (
                                <span style={{ fontSize: '0.72rem', padding: '2px 8px', borderRadius: 999, background: 'rgba(46,125,50,0.35)', color: '#dcedc8' }}>
                                    {infoOrigem.regiao}
                                </span>
                            )}
                        </div>
                        <p style={{ color: '#e2e8f0', fontSize: '0.85rem', margin: 0, lineHeight: 1.45 }}>
                            {infoOrigem.beneficio_texto || infoOrigem.descricao}
                        </p>
                        {infoOrigem.itens && (
                            <p style={{ color: '#94a3b8', fontSize: '0.78rem', margin: 0 }}>
                                <strong>Itens iniciais:</strong> {infoOrigem.itens}
                            </p>
                        )}
                    </div>
                ) : beneficiosOrigem.length === 0 ? (
                    <p style={{ color: '#94a3b8', fontSize: '0.86rem', margin: 0 }}>
                        {origemNome === 'Amnésico'
                            ? 'Amnésico recebe Lembranças Graduais automaticamente e escolhe benefícios com o mestre.'
                            : 'Nenhuma origem selecionada (ou raça sem origem).'}
                    </p>
                ) : (
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                        {beneficiosOrigem.map(ben => {
                            const ativo = escolhasOrigem.includes(ben);
                            const bloqueado = !ativo && escolhasOrigem.length >= 2;
                            return (
                                <button
                                    key={ben}
                                    type="button"
                                    disabled={bloqueado}
                                    onClick={() => handleToggleBeneficioOrigem(ben)}
                                    style={{
                                        padding: '8px 14px',
                                        borderRadius: 8,
                                        border: ativo ? '2px solid #ffd700' : '1px solid #3a4066',
                                        background: ativo ? 'rgba(255, 215, 0, 0.15)' : '#121524',
                                        color: ativo ? '#fff' : bloqueado ? '#555' : '#cbd5e1',
                                        cursor: bloqueado ? 'not-allowed' : 'pointer',
                                        fontWeight: ativo ? 700 : 500,
                                        display: 'inline-flex',
                                        alignItems: 'center',
                                        gap: 6,
                                    }}
                                >
                                    {ativo && <T20Icon name="check" size={14} color="#ffd700" />}
                                    {ben}
                                </button>
                            );
                        })}
                    </div>
                )}
            </div>

            {/* 2. Poder Concedido da Divindade */}
            {deusNome && poderesDeus.length > 0 && (
                <div style={{ background: '#1a1d2e', border: '1px solid #32385a', borderRadius: 10, padding: 18 }}>
                    <h3 style={{ margin: '0 0 12px', color: '#ffd700', fontSize: '1rem', fontFamily: 'Tormenta, serif' }}>
                        Poder Concedido — {deusNome}
                    </h3>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: 10 }}>
                        {poderesDeus.map(nomeP => {
                            const ativo = poderConcedidoAtual === nomeP;
                            const desc = dadosPoderesConcedidos?.[nomeP]?.descricao || '';
                            return (
                                <button
                                    key={nomeP}
                                    type="button"
                                    onClick={() => handleSelectPoderConcedido(nomeP)}
                                    style={{
                                        textAlign: 'left',
                                        padding: 12,
                                        borderRadius: 8,
                                        border: ativo ? '2px solid #ffd700' : '1px solid #3a4066',
                                        background: ativo ? 'rgba(255, 215, 0, 0.14)' : '#121524',
                                        cursor: 'pointer',
                                    }}
                                >
                                    <div style={{ color: ativo ? '#ffd700' : '#f1f5f9', fontWeight: 700, fontSize: '0.92rem', marginBottom: 4 }}>
                                        {nomeP}
                                    </div>
                                    <div style={{ color: '#94a3b8', fontSize: '0.78rem', lineHeight: 1.4 }}>
                                        {desc}
                                    </div>
                                </button>
                            );
                        })}
                    </div>
                </div>
            )}

            {/* 3. Poderes de Classe / Gerais por Nível */}
            <div style={{ background: '#1a1d2e', border: '1px solid #32385a', borderRadius: 10, padding: 18 }}>
                <h3 style={{ margin: '0 0 12px', color: '#ffd700', fontSize: '1rem', fontFamily: 'Tormenta, serif' }}>
                    Poderes de Nível ({poderesClasseAtuais.length} / {slotsPoderes})
                </h3>
                {slotsPoderes === 0 ? (
                    <p style={{ color: '#94a3b8', fontSize: '0.86rem', margin: 0 }}>
                        No 1º nível você ainda não possui slots de poder de classe. Eles são liberados a partir do 2º nível!
                    </p>
                ) : (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                        {Array.from({ length: slotsPoderes }).map((_, i) => {
                            const atual = poderesClasseAtuais[i] || '';
                            return (
                                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                                    <span style={{ width: 55, color: '#94a3b8', fontSize: '0.85rem', fontWeight: 600 }}>Nível {i + 2}</span>
                                    <div style={{ flex: 1, padding: '10px 12px', background: '#121524', border: '1px solid #3a4066', borderRadius: 6, color: atual ? '#fff' : '#64748b' }}>
                                        {atual || 'Nenhum poder selecionado'}
                                    </div>
                                    <button
                                        type="button"
                                        onClick={() => setSlotEmEdicao(i)}
                                        style={{ padding: '9px 14px', borderRadius: 6, border: 'none', background: atual ? '#2e7d32' : '#1976d2', color: '#fff', fontWeight: 700, cursor: 'pointer' }}
                                    >
                                        {atual ? 'Trocar' : 'Escolher'}
                                    </button>
                                </div>
                            );
                        })}
                    </div>
                )}
            </div>

            <PowerSelectorModal
                isOpen={slotEmEdicao !== null}
                onClose={() => setSlotEmEdicao(null)}
                onSelect={handleSelectPoderNivel}
                ficha={ficha}
                listaPoderes={poderesDisponiveisModal}
                listaPericias={listaTodasPericias}
                dadosMagias={dadosMagias}
                dadosHabilidades={dadosHabilidades}
                dadosHabilidadesRaciais={dadosHabilidadesRaciais}
                tipoEscolha="poder"
                titulo={slotEmEdicao !== null ? `Poder de Nível ${slotEmEdicao + 2}` : 'Escolher Poder'}
                itensBloqueados={poderesClasseAtuais.filter((_, idx) => idx !== slotEmEdicao)}
            />
        </div>
    );
}