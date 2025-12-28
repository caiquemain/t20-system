import React, { useState } from 'react';
import type { Personagem } from '../types';

interface OriginSelectorProps {
    ficha: Personagem;
    dadosOrigens: any; // Recebe os dados carregados da API
    updateFicha: (dados: Partial<Personagem>) => void;
    listaTodasPericias: string[];
}

export const OriginSelector: React.FC<OriginSelectorProps> = ({ ficha, dadosOrigens, updateFicha, listaTodasPericias }) => {
    const [mostrarIndisponiveis, setMostrarIndisponiveis] = useState(false);

    const origemNome = ficha.cabecalho.origem;

    // Tenta pegar os dados da origem atual do objeto vindo da API
    const dados = dadosOrigens ? dadosOrigens[origemNome] : null;

    // Se não tiver origem selecionada
    if (!origemNome) return null;

    // Se a origem estiver selecionada mas os dados ainda não carregaram ou não existem
    if (!dados) {
        return (
            <div className="origin-selector-container">
                <div style={{ padding: 10, color: '#aaa', textAlign: 'center', fontStyle: 'italic' }}>
                    {dadosOrigens ?
                        `Dados da origem "${origemNome}" não encontrados.` :
                        "Carregando dados das origens..."}
                </div>
            </div>
        );
    }

    const beneficiosPossiveis = dados.beneficios_lista || [];
    const maxEscolhas = dados.qtd_escolhas || 2;
    const escolhasAtuais = ficha.escolhas_origem || [];

    // --- LÓGICA DE FILTRAGEM ---

    // 1. É Perícia se estiver na lista global de perícias do sistema
    const isPericia = (nome: string) => listaTodasPericias.includes(nome) || nome.startsWith("Ofício");

    // 2. Verifica se já possui (Perícia TREINADA ou Poder na lista de HABILIDADES)
    // Retorna TRUE se o personagem tem o benefício por OUTRA fonte (Raça, Classe, Inteligência)
    const jaPossuiPorOutraFonte = (nome: string) => {
        // Se a escolha atual for essa, não conta como "já possui por fora" (para permitir desmarcar)
        if (escolhasAtuais.includes(nome)) return false;

        if (isPericia(nome)) {
            // Verifica se está treinada na ficha
            return ficha.pericias[nome]?.treino > 0;
        } else {
            // Verifica se tem na lista de habilidades (ex: Poder de Combate pego por Raça)
            return ficha.habilidades.some(h => h.nome === nome);
        }
    };

    // 3. Separação das Listas para Exibição

    // Poderes Disponíveis: Não é perícia E não tem por outra fonte
    const poderesDisponiveis = beneficiosPossiveis.filter((b: string) => !isPericia(b) && !jaPossuiPorOutraFonte(b));

    // Perícias Disponíveis: É perícia E não tem por outra fonte
    const periciasDisponiveis = beneficiosPossiveis.filter((b: string) => isPericia(b) && !jaPossuiPorOutraFonte(b));

    // Indisponíveis: Tudo que já tem por outra fonte (Raça/Classe)
    const itensJaAdquiridos = beneficiosPossiveis.filter((b: string) => jaPossuiPorOutraFonte(b));

    // --- AÇÃO ---
    const toggleBeneficio = (nome: string) => {
        let novasEscolhas = [...escolhasAtuais];

        if (novasEscolhas.includes(nome)) {
            // Remover
            novasEscolhas = novasEscolhas.filter(i => i !== nome);
        } else {
            // Adicionar (se tiver limite)
            if (novasEscolhas.length < maxEscolhas) {
                novasEscolhas.push(nome);
            }
        }
        updateFicha({ escolhas_origem: novasEscolhas });
    };

    // Renderiza uma linha de opção
    const renderRow = (nome: string, tipo: 'Poder' | 'Perícia', disabled: boolean = false) => {
        const selecionado = escolhasAtuais.includes(nome);
        const bloqueado = !selecionado && escolhasAtuais.length >= maxEscolhas;

        return (
            <div
                key={nome}
                className={`origin-option-row ${selecionado ? 'selected' : ''} ${bloqueado || disabled ? 'disabled' : ''}`}
                onClick={() => !disabled && !bloqueado && toggleBeneficio(nome)}
                title={disabled ? "Você já recebeu este benefício de outra fonte (Raça ou Classe)." : ""}
            >
                <div className={`origin-checkbox ${selecionado ? 'checked' : ''}`}>
                    {selecionado && "✔"}
                </div>
                <div className="origin-label">
                    {nome}
                    <div>
                        <span className={`origin-badge ${tipo === 'Poder' ? 'power' : 'skill'}`}>{tipo}</span>
                        {disabled && <span className="origin-badge warning">Já Possui</span>}
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div className="origin-selector-container">
            <div className="origin-header-info">
                <div style={{ flex: 1, paddingRight: 10 }}>
                    <h4 style={{ margin: 0, color: '#eee', fontSize: '1rem' }}>Benefícios de {origemNome}</h4>
                    {dados.descricao && (
                        <small style={{ color: '#888', display: 'block', marginTop: 4, lineHeight: '1.2' }}>
                            {dados.descricao}
                        </small>
                    )}
                    {dados.itens && (
                        <small style={{ color: '#666', display: 'block', marginTop: 4, fontStyle: 'italic' }}>
                            Itens: {dados.itens}
                        </small>
                    )}
                </div>
                <div style={{ textAlign: 'right' }}>
                    <span className={`origin-counter ${escolhasAtuais.length < maxEscolhas ? 'warn' : 'ok'}`}>
                        {escolhasAtuais.length} / {maxEscolhas}
                    </span>
                </div>
            </div>

            {/* 1. PODERES/TALENTOS (Ex: Membro da Igreja, Medicina) */}
            {poderesDisponiveis.length > 0 && (
                <div style={{ marginBottom: 10 }}>
                    <h5 style={{ margin: '0 0 6px 0', fontSize: '0.75rem', color: '#aaa', textTransform: 'uppercase' }}>Poderes & Talentos</h5>
                    {poderesDisponiveis.map((p: string) => renderRow(p, 'Poder'))}
                </div>
            )}

            {/* 2. PERÍCIAS (Ex: Cura, Religião) */}
            {periciasDisponiveis.length > 0 && (
                <div style={{ marginBottom: 10 }}>
                    <h5 style={{ margin: '0 0 6px 0', fontSize: '0.75rem', color: '#aaa', textTransform: 'uppercase' }}>Perícias</h5>
                    {periciasDisponiveis.map((p: string) => renderRow(p, 'Perícia'))}
                </div>
            )}

            {/* 3. JÁ ADQUIRIDOS (Ocultos por padrão) */}
            {itensJaAdquiridos.length > 0 && (
                <div style={{ marginTop: 15, borderTop: '1px dashed #333', paddingTop: 8 }}>
                    <div
                        style={{ fontSize: '0.8rem', color: '#666', cursor: 'pointer', textAlign: 'center', userSelect: 'none' }}
                        onClick={() => setMostrarIndisponiveis(!mostrarIndisponiveis)}
                    >
                        {mostrarIndisponiveis ? "Ocultar" : "Mostrar"} benefícios que você já possui ({itensJaAdquiridos.length}) {mostrarIndisponiveis ? '▲' : '▼'}
                    </div>

                    {mostrarIndisponiveis && (
                        <div style={{ marginTop: 5, opacity: 0.6 }}>
                            {itensJaAdquiridos.map((p: string) => renderRow(p, isPericia(p) ? 'Perícia' : 'Poder', true))}
                        </div>
                    )}
                </div>
            )}

            {/* Mensagem se não houver nada disponível (banco de dados vazio ou erro) */}
            {poderesDisponiveis.length === 0 && periciasDisponiveis.length === 0 && itensJaAdquiridos.length === 0 && (
                <div style={{ padding: 10, textAlign: 'center', color: '#888', background: 'rgba(0,0,0,0.2)', borderRadius: 4 }}>
                    Nenhum benefício listado para esta origem nos dados do sistema.
                </div>
            )}
        </div>
    );
};