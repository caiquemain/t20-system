interface Step {
  id: string;
  label: string;
  icon: string;
}

interface WizardStepperProps {
  steps: Step[];
  currentStep: number;
}

export function WizardStepper({ steps, currentStep }: WizardStepperProps) {
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      gap: '0',
      padding: '20px',
      maxWidth: '1200px',
      margin: '0 auto'
    }}>
      {steps.map((step, index) => {
        const isActive = index === currentStep;
        const isCompleted = index < currentStep;

        return (
          <div key={step.id} style={{ display: 'flex', alignItems: 'center' }}>
            {/* Círculo do Step */}
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: '8px'
            }}>
              <div style={{
                width: '50px',
                height: '50px',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '1.5rem',
                background: isActive ? '#ffd700' : isCompleted ? '#4caf50' : '#444',
                border: `3px solid ${isActive ? '#ffd700' : isCompleted ? '#4caf50' : '#555'}`,
                transition: 'all 0.3s ease',
                boxShadow: isActive ? '0 0 20px rgba(255, 215, 0, 0.5)' : 'none'
              }}>
                {isCompleted ? '✓' : step.icon}
              </div>
              <span style={{
                fontSize: '0.85rem',
                color: isActive ? '#ffd700' : isCompleted ? '#4caf50' : '#888',
                fontWeight: isActive ? 'bold' : 'normal',
                textAlign: 'center',
                maxWidth: '80px'
              }}>
                {step.label}
              </span>
            </div>

            {/* Linha Conectora (exceto no último) */}
            {index < steps.length - 1 && (
              <div style={{
                width: '60px',
                height: '3px',
                background: isCompleted ? '#4caf50' : '#444',
                margin: '0 10px',
                marginBottom: '25px', // Alinha com o centro dos círculos
                transition: 'background 0.3s ease'
              }} />
            )}
          </div>
        );
      })}
    </div>
  );
}