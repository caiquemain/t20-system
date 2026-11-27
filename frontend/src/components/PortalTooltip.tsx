import React, { useState, useRef } from 'react';
import { createPortal } from 'react-dom';

export interface TooltipLinha {
    texto: string;
    cor?: string;
    negrito?: boolean;
    separador?: boolean;
}

interface PortalTooltipProps {
    titulo?: string;
    linhas: TooltipLinha[];
    children: React.ReactNode;
    maxWidth?: number;
}

/**
 * Tooltip renderizada via React Portal em document.body (position: fixed, zIndex: 99999),
 * imune a containers com overflow: hidden / overflow-x: auto (como tabelas e cards).
 */
export const PortalTooltip: React.FC<PortalTooltipProps> = ({
    titulo,
    linhas,
    children,
    maxWidth = 300,
}) => {
    const [visivel, setVisivel] = useState(false);
    const [coords, setCoords] = useState<{ top: number; left: number; abaixo: boolean }>({
        top: 0,
        left: 0,
        abaixo: false,
    });
    const ref = useRef<HTMLSpanElement>(null);

    if (!linhas || linhas.length === 0) {
        return <>{children}</>;
    }

    const abrir = () => {
        if (!ref.current) return;
        const rect = ref.current.getBoundingClientRect();
        const abaixo = rect.top < 170;
        const left = Math.min(
            Math.max(12, rect.left),
            window.innerWidth - maxWidth - 16,
        );
        setCoords({
            top: abaixo ? rect.bottom + 8 : rect.top - 8,
            left,
            abaixo,
        });
        setVisivel(true);
    };

    const fechar = () => setVisivel(false);

    return (
        <span
            ref={ref}
            onMouseEnter={abrir}
            onMouseLeave={fechar}
            style={{ display: 'inline-flex', alignItems: 'center', cursor: 'help' }}
        >
            {children}
            {visivel &&
                createPortal(
                    <div
                        style={{
                            position: 'fixed',
                            top: coords.top,
                            left: coords.left,
                            transform: coords.abaixo ? 'none' : 'translateY(-100%)',
                            width: maxWidth,
                            backgroundColor: '#15151a',
                            border: '1px solid #ffd700',
                            borderRadius: 6,
                            padding: '9px 11px',
                            zIndex: 99999,
                            boxShadow: '0 8px 28px rgba(0, 0, 0, 0.92)',
                            pointerEvents: 'none',
                            textTransform: 'none',
                            fontSize: '0.78rem',
                            lineHeight: 1.4,
                            color: '#ddd',
                        }}
                    >
                        {titulo && (
                            <div
                                style={{
                                    color: '#ffd700',
                                    fontWeight: 'bold',
                                    fontSize: '0.76rem',
                                    textTransform: 'uppercase',
                                    letterSpacing: '0.4px',
                                    borderBottom: '1px solid #333',
                                    paddingBottom: 4,
                                    marginBottom: 6,
                                }}
                            >
                                {titulo}
                            </div>
                        )}
                        {linhas.map((l, idx) => (
                            <div
                                key={idx}
                                style={{
                                    color: l.cor || '#ccc',
                                    fontWeight: l.negrito ? 'bold' : 'normal',
                                    borderTop: l.separador ? '1px dashed #3a3a45' : undefined,
                                    marginTop: l.separador ? 5 : 2,
                                    paddingTop: l.separador ? 5 : 0,
                                }}
                            >
                                {l.texto}
                            </div>
                        ))}
                    </div>,
                    document.body,
                )}
        </span>
    );
};
