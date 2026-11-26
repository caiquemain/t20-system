import type { WizardStepProps } from '../../../types/wizard';
import { T20Icon } from '../../T20Icon';

export function StepPericias(_props: WizardStepProps) {
    return (
        <div>
            <h2 style={{ color: '#ffd700', marginBottom: '20px', display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
                <T20Icon name="arco" size={22} /> Passo 4: Perícias
            </h2>
            <p style={{ color: '#aaa' }}>Em breve: seleção e treinamento de perícias.</p>
        </div>
    );
}