import React, { useMemo, useState } from 'react';
import type { Personagem } from '../types';

export interface PendenciaItem {
    id: string;
    titulo: string;
    detalhe: string;
    acaoLabel: string;
    acao: 'poderes' | 'magias';
    resolvido: boolean;
}

interface LevelUpModalProps {
    isOpen: boolean;
    oculto?: boolean;
    ficha: Personagem;
    onClose: () => void;
    onConfirmLevelUp: () => Promise<{ pvAntes: number; pmAntes: number; circuloAntes: number; habsAntes: string[] } | null>;
    onAbrirConfigHabilidades: () => void;
    onAbrirGrimorio: () => void;
}

function calcularPendencias(ficha: Personagem): PendenciaItem[] {
    const nivelTotal = ficha.cabecalho?.nivel_total || ficha.classes?.[0]?.nivel || 1;
    const classe = ficha.classes?.[0]?.nome || '';
    const subclasse = ficha.classes?.[0]?.subclasse || '';
    const habs = ficha.habilidades || [];
    const lista: PendenciaItem[] = [];

    // 1. Poderes de nível (no T20, 1 poder de classe/geral a partir do 2º nível)
    // Alinhado com ehPoderDeSlotClasse de useFicha.ts (exclui poderes de Origem, Habilidade racial ou Devoção)
    const poderesEsperados = Math.max(0, nivelTotal - 1);
    const poderesEscolhidos = habs.filter(h => {
        const tipo = (h.tipo || '').toString();
        const fonte = (h.fonte || '').toString();
        if (fonte.startsWith('Origem:') || fonte.startsWith('Habilidade:') || fonte.startsWith('Devoção:')) {
            return false;
        }
        return (
            tipo.includes('Poder de') ||
            tipo.includes('Poder Geral') ||
            tipo === 'Poder da Tormenta'
        );
    }).length;

    if (poderesEsperados > 0) {
        const faltam = Math.max(0, poderesEsperados - poderesEscolhidos);
        lista.push({
            id: 'poderes',
            titulo: `Poderes de Classe / Gerais (${poderesEscolhidos}/${poderesEsperados})`,
            detalhe:
                faltam > 0
                    ? `Falta escolher ${faltam} poder(es) para o nível ${nivelTotal}.`
                    : `Todos os ${poderesEsperados} poder(es) de nível escolhidos.`,
            acaoLabel: 'Escolher Poderes',
            acao: 'poderes',
            resolvido: faltam === 0,
        });
    }

    // 2. Magias conhecidas
    const limiteMagias = ficha.combate?.limite_magias || 0;
    const magiasAtuais = (ficha.combate?.magias || []).length;
    if (limiteMagias > 0) {
        const faltamMag = Math.max(0, limiteMagias - magiasAtuais);
        lista.push({
            id: 'magias',
            titulo: `Magias Conhecidas (${magiasAtuais}/${limiteMagias})`,
            detalhe:
                faltamMag > 0
                    ? `Você pode aprender mais ${faltamMag} magia(s) até o ${ficha.combate?.circulo_maximo || 1}º círculo.`
                    : `Grimório completo para o nível ${nivelTotal} (${magiasAtuais}/${limiteMagias}).`,
            acaoLabel: 'Abrir Grimório',
            acao: 'magias',
            resolvido: faltamMag === 0,
        });
    }

    // 3. Devoção (Poder Concedido)
    const deus = (ficha.cabecalho?.deus || '').trim();
    if (deus && !['panteão', 'panteao', 'arton', 'bem'].includes(deus.toLowerCase())) {
        const temPoderDevocao = habs.some(
            h => (h.tipo || '').toLowerCase().includes('concedido') || (h.fonte || '').toLowerCase().includes('devoção')
        );
        if (!temPoderDevocao) {
            lista.push({
                id: 'devocao',
                titulo: `Poder Concedido (${deus})`,
                detalhe: `Você é devoto de ${deus}, mas ainda não escolheu seu Poder Concedido.`,
                acaoLabel: 'Escolher Devoção',
                acao: 'poderes',
                resolvido: false,
            });
        }
    }

    // 4. Arcanista sem Caminho ou Feiticeiro sem Linhagem
    if (classe === 'Arcanista' && !subclasse) {
        lista.push({
            id: 'subclasse',
            titulo: 'Caminho do Arcanista',
            detalhe: 'Escolha seu Caminho (Bruxo, Feiticeiro ou Mago).',
            acaoLabel: 'Configurar Caminho',
            acao: 'poderes',
            resolvido: false,
        });
    } else if (classe === 'Arcanista' && subclasse === 'Feiticeiro') {
        const temLinhagem = habs.some(h => (h.nome || '').startsWith('Linhagem '));
        if (!temLinhagem) {
            lista.push({
                id: 'linhagem',
                titulo: 'Linhagem Sobrenatural (Feiticeiro)',
                detalhe: 'Escolha sua Linhagem (Dracônica, Feérica, Rubra ou Abençoada).',
                acaoLabel: 'Escolher Linhagem',
                acao: 'poderes',
                resolvido: false,
            });
        }
    }

    return lista;
}

export const LevelUpModal: React.FC<LevelUpModalProps> = ({
    isOpen,
    oculto = false,
    ficha,
    onClose,
    onConfirmLevelUp,
    onAbrirConfigHabilidades,
    onAbrirGrimorio,
}) => {
    const [etapa, setEtapa] = useState<'pendencias' | 'novo_nivel'>('pendencias');
    const [subindo, setSubindo] = useState(false);
    const [snapshotAntes, setSnapshotAntes] = useState<{
        pvAntes: number;
        pmAntes: number;
        circuloAntes: number;
        habsAntes: string[];
    } | null>(null);

    const pendencias = useMemo(() => calcularPendencias(ficha), [ficha]);
    const pendentesAbertas = pendencias.filter(p => !p.resolvido);
    const nivelAtual = ficha.classes?.[0]?.nivel || 1;
    const classeAtual = ficha.classes?.[0]?.nome || 'Classe';

    if (!isOpen) return null;

    const handleSubir = async () => {
        if (subindo) return;
        setSubindo(true);
        try {
            const snap = await onConfirmLevelUp();
            if (snap) {
                setSnapshotAntes(snap);
                setEtapa('novo_nivel');
            }
        } finally {
            setSubindo(false);
        }
    };

    const handleFechar = () => {
        setEtapa('pendencias');
        setSnapshotAntes(null);
        onClose();
    };

    const deltaPv = snapshotAntes ? ficha.status.pv.maximo - snapshotAntes.pvAntes : 0;
    const deltaPm = snapshotAntes ? ficha.status.pm.maximo - snapshotAntes.pmAntes : 0;
    const novoCirculo =
        snapshotAntes && (ficha.combate.circulo_maximo || 0) > snapshotAntes.circuloAntes
            ? ficha.combate.circulo_maximo
            : null;
    const novasHabs = snapshotAntes
        ? (ficha.habilidades || [])
              .map(h => h.nome)
              .filter(n => !snapshotAntes.habsAntes.includes(n))
        : [];

    return (
        <div
            onClick={handleFechar}
            style={{
                position: 'fixed',
                inset: 0,
                background: 'rgba(0,0,0,0.82)',
                zIndex: 9500,
                display: oculto ? 'none' : 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: 16,
            }}
        >
            <div
                onClick={e => e.stopPropagation()}
                style={{
                    width: '100%',
                    maxWidth: 640,
                    maxHeight: '88vh',
                    overflowY: 'auto',
                    background: '#16161e',
                    border: `1px solid ${etapa === 'novo_nivel' ? '#4caf50' : '#ce93d8'}`,
                    borderRadius: 10,
                    padding: 22,
                    color: '#eee',
                    boxShadow: '0 10px 36px rgba(0,0,0,0.85)',
                }}
            >
                {etapa === 'pendencias' ? (
                    <>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 14 }}>
                            <div>
                                <div style={{ fontSize: '0.75rem', color: '#ce93d8', textTransform: 'uppercase', letterSpacing: '0.6px' }}>
                                    Etapa 1 de 2 — Conferência antes de subir
                                </div>
                                <h2 style={{ margin: '4px 0 0', color: '#fff', fontSize: '1.25rem' }}>
                                    Subir {classeAtual} do Nível {nivelAtual} → {nivelAtual + 1}
                                </h2>
                            </div>
                            <button
                                onClick={handleFechar}
                                style={{ background: '#2a2a36', color: '#ccc', border: '1px solid #444', borderRadius: 6, padding: '5px 10px', cursor: 'pointer' }}
                            >
                                ✕
                            </button>
                        </div>

                        {pendentesAbertas.length > 0 ? (
                            <div style={{ background: 'rgba(255, 183, 77, 0.1)', border: '1px solid rgba(255, 183, 77, 0.45)', borderRadius: 8, padding: 12, marginBottom: 16 }}>
                                <strong style={{ color: '#ffb74d', display: 'block', marginBottom: 4 }}>
                                    ⚠ Você ainda tem {pendentesAbertas.length} pendência(s) do Nível {nivelAtual}:
                                </strong>
                                <span style={{ fontSize: '0.82rem', color: '#ddd' }}>
                                    Resolva o que faltou do nível atual usando os botões abaixo — o checklist atualiza automaticamente!
                                </span>
                            </div>
                        ) : (
                            <div style={{ background: 'rgba(76, 175, 80, 0.12)', border: '1px solid rgba(76, 175, 80, 0.45)', borderRadius: 8, padding: 12, marginBottom: 16, color: '#a5d6a7', fontSize: '0.86rem' }}>
                                ✅ Tudo certo no Nível {nivelAtual}! Nenhuma pendência encontrada. Pronto para subir para o Nível {nivelAtual + 1}.
                            </div>
                        )}

                        {pendencias.length > 0 && (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginBottom: 18 }}>
                                {pendencias.map(p => (
                                    <div
                                        key={p.id}
                                        style={{
                                            display: 'flex',
                                            justifyContent: 'space-between',
                                            alignItems: 'center',
                                            gap: 12,
                                            padding: '10px 12px',
                                            borderRadius: 6,
                                            background: p.resolvido ? 'rgba(76,175,80,0.08)' : '#1f1f2b',
                                            border: `1px solid ${p.resolvido ? 'rgba(76,175,80,0.35)' : '#444'}`,
                                        }}
                                    >
                                        <div>
                                            <div style={{ fontWeight: 'bold', fontSize: '0.9rem', color: p.resolvido ? '#81c784' : '#ffd54f' }}>
                                                {p.resolvido ? '✓ ' : '• '}
                                                {p.titulo}
                                            </div>
                                            <div style={{ fontSize: '0.8rem', color: '#bbb', marginTop: 2 }}>{p.detalhe}</div>
                                        </div>
                                        {!p.resolvido && (
                                            <button
                                                type="button"
                                                onClick={() => (p.acao === 'magias' ? onAbrirGrimorio() : onAbrirConfigHabilidades())}
                                                style={{
                                                    background: '#ffd700',
                                                    color: '#111',
                                                    border: 'none',
                                                    borderRadius: 6,
                                                    padding: '7px 12px',
                                                    fontWeight: 'bold',
                                                    cursor: 'pointer',
                                                    whiteSpace: 'nowrap',
                                                    fontSize: '0.8rem',
                                                }}
                                            >
                                                {p.acaoLabel}
                                            </button>
                                        )}
                                    </div>
                                ))}
                            </div>
                        )}

                        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 10 }}>
                            <button
                                onClick={handleFechar}
                                style={{ background: '#2a2a36', color: '#ccc', border: '1px solid #444', borderRadius: 6, padding: '9px 16px', cursor: 'pointer' }}
                            >
                                Cancelar
                            </button>
                            <button
                                onClick={handleSubir}
                                disabled={subindo}
                                style={{
                                    background: pendentesAbertas.length > 0 ? '#7b1fa2' : '#9c27b0',
                                    color: '#fff',
                                    border: 'none',
                                    borderRadius: 6,
                                    padding: '9px 18px',
                                    fontWeight: 'bold',
                                    cursor: subindo ? 'wait' : 'pointer',
                                }}
                            >
                                {subindo
                                    ? 'Subindo de nível...'
                                    : pendentesAbertas.length > 0
                                      ? `Avançar mesmo assim para Nível ${nivelAtual + 1} →`
                                      : `Subir para o Nível ${nivelAtual + 1} →`}
                            </button>
                        </div>
                    </>
                ) : (
                    <>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 14 }}>
                            <div>
                                <div style={{ fontSize: '0.75rem', color: '#81c784', textTransform: 'uppercase', letterSpacing: '0.6px' }}>
                                    Etapa 2 de 2 — Escolhas do Novo Nível
                                </div>
                                <h2 style={{ margin: '4px 0 0', color: '#ffd700', fontSize: '1.3rem' }}>
                                    🎉 Bem-vindo ao Nível {nivelAtual}!
                                </h2>
                            </div>
                            <button
                                onClick={handleFechar}
                                style={{ background: '#2a2a36', color: '#ccc', border: '1px solid #444', borderRadius: 6, padding: '5px 10px', cursor: 'pointer' }}
                            >
                                ✕
                            </button>
                        </div>

                        {/* Ganhos automáticos */}
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: 10, marginBottom: 16 }}>
                            <div style={{ background: '#1e2820', border: '1px solid #2e7d32', borderRadius: 8, padding: 10, textAlign: 'center' }}>
                                <div style={{ fontSize: '0.72rem', color: '#a5d6a7' }}>PV MÁXIMO</div>
                                <div style={{ fontSize: '1.15rem', fontWeight: 'bold', color: '#81c784' }}>
                                    {ficha.status.pv.maximo} {deltaPv > 0 ? `(+${deltaPv})` : ''}
                                </div>
                            </div>
                            <div style={{ background: '#1c2330', border: '1px solid #1565c0', borderRadius: 8, padding: 10, textAlign: 'center' }}>
                                <div style={{ fontSize: '0.72rem', color: '#90caf9' }}>PM MÁXIMO</div>
                                <div style={{ fontSize: '1.15rem', fontWeight: 'bold', color: '#64b5f6' }}>
                                    {ficha.status.pm.maximo} {deltaPm > 0 ? `(+${deltaPm})` : ''}
                                </div>
                            </div>
                            {novoCirculo && (
                                <div style={{ background: '#281c30', border: '1px solid #9c27b0', borderRadius: 8, padding: 10, textAlign: 'center' }}>
                                    <div style={{ fontSize: '0.72rem', color: '#ce93d8' }}>NOVO CÍRCULO</div>
                                    <div style={{ fontSize: '1.15rem', fontWeight: 'bold', color: '#e1bee7' }}>
                                        {novoCirculo}º Círculo!
                                    </div>
                                </div>
                            )}
                        </div>

                        {novasHabs.length > 0 && (
                            <div style={{ background: 'rgba(128,222,234,0.08)', border: '1px solid rgba(128,222,234,0.3)', borderRadius: 6, padding: 10, marginBottom: 14, fontSize: '0.82rem' }}>
                                <strong style={{ color: '#80deea' }}>Novas habilidades automáticas ganhas:</strong>{' '}
                                <span style={{ color: '#eee' }}>{novasHabs.join(', ')}</span>
                            </div>
                        )}

                        <div style={{ marginBottom: 18 }}>
                            <strong style={{ color: '#ffd700', display: 'block', marginBottom: 8, fontSize: '0.9rem' }}>
                                Escolha seus ganhos do Nível {nivelAtual}:
                            </strong>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                                {pendencias.map(p => (
                                    <div
                                        key={p.id}
                                        style={{
                                            display: 'flex',
                                            justifyContent: 'space-between',
                                            alignItems: 'center',
                                            gap: 12,
                                            padding: '10px 12px',
                                            borderRadius: 6,
                                            background: p.resolvido ? 'rgba(76,175,80,0.08)' : '#1f1f2b',
                                            border: `1px solid ${p.resolvido ? 'rgba(76,175,80,0.4)' : '#ffd70088'}`,
                                        }}
                                    >
                                        <div>
                                            <div style={{ fontWeight: 'bold', fontSize: '0.9rem', color: p.resolvido ? '#81c784' : '#ffd54f' }}>
                                                {p.resolvido ? '✓ ' : '★ '}
                                                {p.titulo}
                                            </div>
                                            <div style={{ fontSize: '0.8rem', color: '#bbb', marginTop: 2 }}>{p.detalhe}</div>
                                        </div>
                                        <button
                                            type="button"
                                            onClick={() => (p.acao === 'magias' ? onAbrirGrimorio() : onAbrirConfigHabilidades())}
                                            style={{
                                                background: p.resolvido ? '#2c2c38' : '#ffd700',
                                                color: p.resolvido ? '#ccc' : '#111',
                                                border: p.resolvido ? '1px solid #444' : 'none',
                                                borderRadius: 6,
                                                padding: '7px 12px',
                                                fontWeight: 'bold',
                                                cursor: 'pointer',
                                                whiteSpace: 'nowrap',
                                                fontSize: '0.8rem',
                                            }}
                                        >
                                            {p.resolvido ? 'Editar' : p.acaoLabel}
                                        </button>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                            <button
                                onClick={handleFechar}
                                style={{
                                    background: '#4caf50',
                                    color: '#fff',
                                    border: 'none',
                                    borderRadius: 6,
                                    padding: '10px 22px',
                                    fontWeight: 'bold',
                                    cursor: 'pointer',
                                }}
                            >
                                {pendentesAbertas.length === 0 ? '✓ Concluir Level-Up' : 'Fechar e continuar depois'}
                            </button>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};
