import type { WizardStepProps } from '../../../types/wizard';
import { T20Icon } from '../../T20Icon';

export function StepMagias(_props: WizardStepProps) {
    return (
        <div>
            <h2 style={{ color: '#ffd700', marginBottom: '20px', display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
                <T20Icon name="grimorio" size={22} /> Passo 6: Magias
            </h2>
            <p style={{ color: '#aaa' }}>Em breve: grimório e seleção de magias.</p>
        </div>
    );
}