import type { WizardStepProps } from '../../../types/wizard';
import { T20Icon } from '../../T20Icon';

export function StepPoderes(_props: WizardStepProps) {
    return (
        <div>
            <h2 style={{ color: '#ffd700', marginBottom: '20px', display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
                <T20Icon name="efeito" size={22} /> Passo 5: Poderes
            </h2>
            <p style={{ color: '#aaa' }}>Em breve: seleção de poderes gerais, de classe e raciais.</p>
        </div>
    );
}