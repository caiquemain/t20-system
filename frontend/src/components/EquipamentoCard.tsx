import React, { useState, useMemo } from 'react';
import { EntitySelectorModal, type EntityItem } from './EntitySelectorModal';

interface Item {
    nome: string;
    qtd: number;
    espaco: number;
    descricao?: string;
    tipo: string;
    equipado: boolean;
}

interface Inventario {
    dinheiro: { tibares: number; cobre: number; ouro: number };
    equipamentos: Item[];
    carga_total: number;
    carga_maxima: number;
    sobrecargado: boolean;
}

interface DadosEquipamentos {
    armas: Record<string, any>;
    armaduras: Record<string, any>;
}

interface EquipamentoCardProps {
    inventario: Inventario;
    dadosEquipamentos: DadosEquipamentos;
    onUpdateInventario: (novoInventario: Inventario) => void;
}

export const EquipamentoCard: React.FC<EquipamentoCardProps> = ({
    inventario,
    dadosEquipamentos,
    onUpdateInventario,
}) => {
    const [modalAberto, setModalAberto] = useState(false);
    const [filtroCategoria, setFiltroCategoria] = useState<string>('todas');
    const [filtroProposito, setFiltroProposito] = useState<string>('todos');
    const [filtroTipo, setFiltroTipo] = useState<string>('todos');

    const { equipamentos, carga_total, carga_maxima, sobrecargado, dinheiro } = inventario;

    // Contadores para limites T20
    const empunhados = equipamentos.filter(i => {
        const cat = dadosEquipamentos.armas[i.nome] || dadosEquipamentos.armaduras[i.nome];
        return i.equipado && (cat?.proposito === 'Corpo a Corpo' || cat?.proposito === 'À Distância');
    }).length;

    const armadurasVestidas = equipamentos.filter(i => {
        const cat = dadosEquipamentos.armaduras[i.nome];
        return i.equipado && cat?.tipo_armadura !== 'Escudo';
    }).length;

    const escudosEmpunhados = equipamentos.filter(i => {
        const cat = dadosEquipamentos.armaduras[i.nome];
        return i.equipado && cat?.tipo_armadura === 'Escudo';
    }).length;

    // Cor da barra de carga
    const corCarga = sobrecargado ? '#ff5252' : carga_total > carga_maxima * 0.8 ? '#ffa726' : '#66bb6a';
    const percentual = carga_maxima > 0 ? Math.min(100, (carga_total / carga_maxima) * 100) : 0;

    // Catálogo filtrado
    const catalogoItens: EntityItem[] = useMemo(() => {
        const itens: EntityItem[] = [];
        
        // Armas
        Object.entries(dadosEquipamentos.armas || {}).forEach(([nome, dados]: [string, any]) => {
            if (filtroCategoria !== 'todas' && dados.categoria !== filtroCategoria) return;
            if (filtroProposito !== 'todos' && dados.proposito !== filtroProposito) return;
            
            const props: string[] = [];
            if (dados.dano) props.push(`${dados.dano} ${dados.tipo || ''}`);
            if (dados.arremessavel) props.push('Arremessável');
            if (dados.habilidades?.includes('versátil')) props.push(`Versátil ${dados.versatil || ''}`);
            if (dados.habilidades?.includes('alongada')) props.push('Alongada');
            if (dados.habilidades?.includes('ágil')) props.push('Ágil');
            if (dados.habilidades?.includes('dupla')) props.push('Dupla');
            
            const tooltip = [
                `Preço: T$ ${dados.preco}`,
                `Empunhadura: ${dados.empunhadura}`,
                `Crítico: ${dados.critico}`,
                dados.alcance ? `Alcance: ${dados.alcance}` : '',
                props.length > 0 ? `Propriedades: ${props.join(', ')}` : ''
            ].filter(Boolean).join(' • ');

            itens.push({
                nome,
                bonus: dados.dano ? `${dados.dano} ${dados.tipo || ''}` : undefined,
                descricao: `${dados.categoria} · ${dados.empunhadura} · ${dados.espacos} esp`,
                icone: '⚔️',
                tooltip
            });
        });

        // Armaduras
        Object.entries(dadosEquipamentos.armaduras || {}).forEach(([nome, dados]: [string, any]) => {
            if (filtroTipo !== 'todos' && dados.tipo_armadura !== filtroTipo) return;
            
            const tooltip = [
                `Preço: T$ ${dados.preco}`,
                `Bônus: +${dados.bonus_defesa} Defesa`,
                `Penalidade: ${dados.penalidade_armadura}`,
                `Espaços: ${dados.espacos}`
            ].join(' • ');

            itens.push({
                nome,
                bonus: `+${dados.bonus_defesa} Defesa`,
                descricao: `${dados.tipo_armadura} · ${dados.espacos} esp`,
                icone: '🛡️',
                tooltip
            });
        });

        return itens;
    }, [dadosEquipamentos, filtroCategoria, filtroProposito, filtroTipo]);

    const adicionarItem = (nome: string) => {
        const cat = dadosEquipamentos.armas[nome] || dadosEquipamentos.armaduras[nome];
        if (!cat) return;

        const novoItem: Item = {
            nome,
            qtd: 1,
            espaco: cat.espacos || 1,
            descricao: cat.descricao || '',
            tipo: dadosEquipamentos.armas[nome] ? 'Arma' : 'Armadura',
            equipado: false,
        };

        onUpdateInventario({
            ...inventario,
            equipamentos: [...equipamentos, novoItem],
        });
        setModalAberto(false);
    };

    const toggleEquipado = (index: number) => {
        const novos = [...equipamentos];
        const item = { ...novos[index] };
        const cat = dadosEquipamentos.armas[item.nome] || dadosEquipamentos.armaduras[item.nome];

        if (!cat) return;

        // Limites T20
        if (!item.equipado) {
            if (cat.proposito === 'Corpo a Corpo' || cat.proposito === 'À Distância') {
                if (empunhados >= 2) {
                    alert('Limite de 2 itens empunhados (1 por mão)');
                    return;
                }
            }
            if (cat.tipo_armadura && cat.tipo_armadura !== 'Escudo') {
                if (armadurasVestidas >= 1) {
                    alert('Limite de 1 armadura vestida');
                    return;
                }
            }
            if (cat.tipo_armadura === 'Escudo') {
                if (escudosEmpunhados >= 1) {
                    alert('Limite de 1 escudo empunhado');
                    return;
                }
            }
        }

        item.equipado = !item.equipado;
        novos[index] = item;
        onUpdateInventario({ ...inventario, equipamentos: novos });
    };

    const removerItem = (index: number) => {
        const novos = equipamentos.filter((_, i) => i !== index);
        onUpdateInventario({ ...inventario, equipamentos: novos });
    };

    const alterarQuantidade = (index: number, delta: number) => {
        const novos = [...equipamentos];
        const item = { ...novos[index] };
        item.qtd = Math.max(1, item.qtd + delta);
        novos[index] = item;
        onUpdateInventario({ ...inventario, equipamentos: novos });
    };

    const getBadgeEstado = (item: Item) => {
        const cat = dadosEquipamentos.armas[item.nome] || dadosEquipamentos.armaduras[item.nome];
        if (!item.equipado) return { label: 'Guardada', cor: '#666' };
        if (cat?.proposito) return { label: 'Empunhada', cor: '#ff9800' };
        if (cat?.tipo_armadura === 'Escudo') return { label: 'Empunhado', cor: '#ff9800' };
        if (cat?.tipo_armadura) return { label: 'Vestida', cor: '#4caf50' };
        return { label: 'Equipada', cor: '#2196f3' };
    };

    return (
        <>
            <div className="section-card" style={{ marginBottom: 20 }}>
                <h3 className="section-title" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    🎒 Equipamento
                    <button
                        className="btn-action"
                        onClick={() => setModalAberto(true)}
                        style={{ padding: '6px 12px', fontSize: '0.85rem' }}
                    >
                        + Adicionar Item
                    </button>
                </h3>

                {/* Barra de Carga */}
                <div style={{ marginBottom: 15 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 5 }}>
                        <span style={{ fontSize: '0.9rem', fontWeight: 'bold' }}>
                            CARGA: {carga_total} / {carga_maxima}
                        </span>
                        {sobrecargado && (
                            <span style={{
                                background: '#ff5252',
                                color: 'white',
                                padding: '2px 8px',
                                borderRadius: 4,
                                fontSize: '0.75rem',
                                fontWeight: 'bold',
                                animation: 'pulse 1.5s infinite'
                            }}>
                                SOBRECARGADO
                            </span>
                        )}
                    </div>
                    <div style={{
                        width: '100%',
                        height: 8,
                        background: '#1a1a1a',
                        borderRadius: 4,
                        overflow: 'hidden'
                    }}>
                        <div style={{
                            width: `${percentual}%`,
                            height: '100%',
                            background: corCarga,
                            transition: 'all 0.3s'
                        }} />
                    </div>
                </div>

                {/* Dinheiro */}
                {dinheiro && (dinheiro.ouro > 0 || dinheiro.tibares > 0 || dinheiro.cobre > 0) && (
                    <div style={{
                        background: 'rgba(0,0,0,0.3)',
                        padding: '8px 12px',
                        borderRadius: 4,
                        marginBottom: 15,
                        display: 'flex',
                        gap: 15,
                        fontSize: '0.85rem'
                    }}>
                        {dinheiro.ouro > 0 && <span style={{ color: '#ffd700' }}>🪙 {dinheiro.ouro} TO</span>}
                        {dinheiro.tibares > 0 && <span style={{ color: '#c0c0c0' }}>🪙 {dinheiro.tibares} T$</span>}
                        {dinheiro.cobre > 0 && <span style={{ color: '#cd7f32' }}>🪙 {dinheiro.cobre} TC</span>}
                    </div>
                )}

                {/* Lista de Itens */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                    {equipamentos.length === 0 ? (
                        <p style={{ color: '#666', textAlign: 'center', padding: 20, margin: 0 }}>
                            Nenhum item no inventário
                        </p>
                    ) : (
                        equipamentos.map((item, i) => {
                            const cat = dadosEquipamentos.armas[item.nome] || dadosEquipamentos.armaduras[item.nome];
                            const badge = getBadgeEstado(item);
                            const icon = dadosEquipamentos.armas[item.nome] ? '⚔️' : 
                                        (cat?.tipo_armadura === 'Escudo' ? '🛡️' : 
                                        (cat?.tipo_armadura ? '🛡️' : '🎒'));

                            return (
                                <div key={i} style={{
                                    background: 'rgba(0,0,0,0.3)',
                                    padding: 10,
                                    borderRadius: 4,
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: 10
                                }}>
                                    <span style={{ fontSize: '1.2rem' }}>{icon}</span>
                                    <div style={{ flex: 1 }}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                            <strong style={{ fontSize: '0.95rem' }}>{item.nome}</strong>
                                            <span style={{
                                                fontSize: '0.7rem',
                                                padding: '2px 6px',
                                                borderRadius: 3,
                                                background: badge.cor,
                                                color: 'white'
                                            }}>
                                                {badge.label}
                                            </span>
                                        </div>
                                        {cat && (
                                            <div style={{ fontSize: '0.75rem', color: '#888', marginTop: 2 }}>
                                                {cat.dano && <span>{cat.dano} {cat.tipo} · </span>}
                                                {cat.bonus_defesa && <span>+{cat.bonus_defesa} Def · </span>}
                                                {cat.espacos || item.espaco} espaço(s)
                                            </div>
                                        )}
                                    </div>
                                    {item.qtd > 1 && (
                                        <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                                            <button
                                                onClick={() => alterarQuantidade(i, -1)}
                                                style={{
                                                    background: '#333',
                                                    border: 'none',
                                                    color: 'white',
                                                    width: 20,
                                                    height: 20,
                                                    borderRadius: 3,
                                                    cursor: 'pointer',
                                                    fontSize: '0.9rem'
                                                }}
                                            >−</button>
                                            <span style={{ fontSize: '0.9rem', minWidth: 20, textAlign: 'center' }}>
                                                {item.qtd}
                                            </span>
                                            <button
                                                onClick={() => alterarQuantidade(i, 1)}
                                                style={{
                                                    background: '#333',
                                                    border: 'none',
                                                    color: 'white',
                                                    width: 20,
                                                    height: 20,
                                                    borderRadius: 3,
                                                    cursor: 'pointer',
                                                    fontSize: '0.9rem'
                                                }}
                                            >+</button>
                                        </div>
                                    )}
                                    <button
                                        onClick={() => toggleEquipado(i)}
                                        style={{
                                            background: item.equipado ? '#ff9800' : '#4caf50',
                                            border: 'none',
                                            color: 'white',
                                            padding: '4px 10px',
                                            borderRadius: 3,
                                            cursor: 'pointer',
                                            fontSize: '0.8rem'
                                        }}
                                    >
                                        {item.equipado ? 'Remover' : 'Equipar'}
                                    </button>
                                    <button
                                        onClick={() => removerItem(i)}
                                        style={{
                                            background: '#ff5252',
                                            border: 'none',
                                            color: 'white',
                                            width: 24,
                                            height: 24,
                                            borderRadius: 3,
                                            cursor: 'pointer',
                                            fontSize: '0.9rem'
                                        }}
                                    >🗑️</button>
                                </div>
                            );
                        })
                    )}
                </div>
            </div>

            {/* Modal com Filtros */}
            {modalAberto && (
                <div style={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    background: 'rgba(0,0,0,0.8)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    zIndex: 9999
                }}>
                    <div style={{
                        background: '#1e1e1e',
                        borderRadius: 8,
                        padding: 20,
                        maxWidth: '90%',
                        maxHeight: '90vh',
                        width: '800px',
                        display: 'flex',
                        flexDirection: 'column'
                    }}>
                        <div style={{ marginBottom: 15 }}>
                            <h2 style={{ margin: '0 0 15px 0' }}>🎒 Adicionar Item</h2>
                            
                            {/* Filtros */}
                            <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginBottom: 15 }}>
                                <select
                                    value={filtroCategoria}
                                    onChange={(e) => setFiltroCategoria(e.target.value)}
                                    style={{ padding: '6px 10px', borderRadius: 4, background: '#333', color: 'white', border: 'none' }}
                                >
                                    <option value="todas">Todas Categorias</option>
                                    <option value="Simples">Simples</option>
                                    <option value="Marcial">Marcial</option>
                                    <option value="Exótica">Exótica</option>
                                    <option value="Fogo">Fogo</option>
                                </select>
                                
                                <select
                                    value={filtroProposito}
                                    onChange={(e) => setFiltroProposito(e.target.value)}
                                    style={{ padding: '6px 10px', borderRadius: 4, background: '#333', color: 'white', border: 'none' }}
                                >
                                    <option value="todos">Todos Propósitos</option>
                                    <option value="Corpo a Corpo">Corpo a Corpo</option>
                                    <option value="À Distância">À Distância</option>
                                </select>
                                
                                <select
                                    value={filtroTipo}
                                    onChange={(e) => setFiltroTipo(e.target.value)}
                                    style={{ padding: '6px 10px', borderRadius: 4, background: '#333', color: 'white', border: 'none' }}
                                >
                                    <option value="todos">Todos Tipos</option>
                                    <option value="Leve">Armadura Leve</option>
                                    <option value="Pesada">Armadura Pesada</option>
                                    <option value="Escudo">Escudo</option>
                                </select>
                            </div>
                        </div>

                        <div style={{ flex: 1, overflowY: 'auto', marginBottom: 15 }}>
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 10 }}>
                                {catalogoItens.map((item, i) => (
                                    <div
                                        key={i}
                                        onClick={() => adicionarItem(item.nome)}
                                        title={item.tooltip}
                                        style={{
                                            background: '#252525',
                                            padding: 12,
                                            borderRadius: 6,
                                            cursor: 'pointer',
                                            border: '2px solid #333',
                                            transition: 'all 0.2s'
                                        }}
                                        onMouseEnter={(e) => e.currentTarget.style.borderColor = '#ffd700'}
                                        onMouseLeave={(e) => e.currentTarget.style.borderColor = '#333'}
                                    >
                                        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
                                            <span style={{ fontSize: '1.2rem' }}>{item.icone}</span>
                                            <strong style={{ fontSize: '0.9rem' }}>{item.nome}</strong>
                                        </div>
                                        {item.bonus && (
                                            <div style={{ fontSize: '0.8rem', color: '#80deea', marginBottom: 4 }}>
                                                {item.bonus}
                                            </div>
                                        )}
                                        <div style={{ fontSize: '0.75rem', color: '#888' }}>
                                            {item.descricao}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <button
                            onClick={() => setModalAberto(false)}
                            style={{
                                background: '#ff5252',
                                border: 'none',
                                color: 'white',
                                padding: '8px 16px',
                                borderRadius: 4,
                                cursor: 'pointer',
                                fontSize: '0.9rem'
                            }}
                        >
                            Cancelar
                        </button>
                    </div>
                </div>
            )}
        </>
    );
};
