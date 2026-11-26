import { useEffect, useRef } from 'react';

// Pilha LIFO global para garantir que apertar ESC feche apenas o modal mais acima
const escapeStack: Array<() => void> = [];
let listenerRegistered = false;

function handleGlobalKeyDown(e: KeyboardEvent) {
    if (e.key !== 'Escape') return;
    if (escapeStack.length === 0) return;
    const topClose = escapeStack[escapeStack.length - 1];
    if (topClose) {
        e.preventDefault();
        topClose();
    }
}

function ensureListener() {
    if (!listenerRegistered && typeof window !== 'undefined') {
        window.addEventListener('keydown', handleGlobalKeyDown);
        listenerRegistered = true;
    }
}

export function useEscapeKey(active: boolean, onClose: () => void) {
    const onCloseRef = useRef(onClose);
    onCloseRef.current = onClose;

    useEffect(() => {
        if (!active) return;
        ensureListener();
        const handler = () => onCloseRef.current();
        escapeStack.push(handler);
        return () => {
            const idx = escapeStack.lastIndexOf(handler);
            if (idx !== -1) escapeStack.splice(idx, 1);
        };
    }, [active]);
}
