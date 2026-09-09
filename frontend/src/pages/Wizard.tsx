import { useState, useEffect, useRef } from 'react';
import { createPersonagem } from '../services/api';
import { useNavigate, useParams } from 'react-router-dom';
import { useFicha } from '../hooks/useFicha';
import { WizardStepper } from '../components/wizard/WizardStepper';

// Importar os Steps (vamos criar em seguida)
import { StepConceito } from '../components/wizard/steps/StepConceito';
import { StepAtributos } from '../components/wizard/steps/StepAtributos';
import { StepClasse } from '../components/wizard/steps/StepClasse';
import { StepPericias } from '../components/wizard/steps/StepPericias';
import { StepPoderes } from '../components/wizard/steps/StepPoderes';
import { StepMagias } from '../components/wizard/steps/StepMagias';
import { StepRevisao } from '../components/wizard/steps/StepRevisao';

const WIZARD_STEPS = [
  { id: 'conceito', label: 'Conceito', icon: '📝' },
  { id: 'atributos', label: 'Atributos', icon: '💪' },
  { id: 'classe', label: 'Classe', icon: '⚔️' },
  { id: 'pericias', label: 'Perícias', icon: '🎯' },
  { id: 'poderes', label: 'Poderes', icon: '✨' },
  { id: 'magias', label: 'Magias', icon: '📖' },
  { id: 'revisao', label: 'Revisão', icon: '✅' },
];

function Wizard() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(0);
      const criandoRef = useRef(false);

    useEffect(() => {
        if (id || criandoRef.current) return;
        criandoRef.current = true;
        (async () => {
            try {
                const res = await createPersonagem({
                    cabecalho: { nome: "Novo Aventureiro", raca: "", origem: "", deus: "", nivel_total: 1 },
                    classes: [{ nome: "Guerreiro", nivel: 1, primaria: true }],
                    atributos_base: { forca: 0, destreza: 0, constituicao: 0, inteligencia: 0, sabedoria: 0, carisma: 0 }
                } as any);
                navigate(`/wizard/${res.data._id}`, { replace: true });
            } catch (e) {
                console.error("Erro ao criar ficha do wizard", e);
            }
        })();
    }, [id, navigate]);

  // 🔄 Reutiliza o hook que já temos!
  const {
    ficha,
    loading,
    updateFicha,
    // Dados estáticos
    listaRacas, listaClasses, listaOrigens, listaTodasPericias,
    listaPoderes, listaDeuses,
    dadosRacas, dadosClasses, dadosOrigens, dadosHabilidadesClasse,
    dadosMagias, dadosHabilidades, dadosDeuses, dadosPoderesConcedidos,
    dadosHabilidadesRaciais,
    // Funções de regra
    handleAtributoBaseChange,
    montarHabilidadesParaPanel,
    handleSaveEscolhas,
  } = useFicha(id);

  if (loading || !ficha) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        fontSize: '1.5rem',
        color: '#888'
      }}>
        ⏳ Carregando grimório...
      </div>
    );
  }

  const handleNext = () => {
    if (currentStep < WIZARD_STEPS.length - 1) {
      setCurrentStep(currentStep + 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handleFinish = () => {
    // Redireciona para a ficha completa após finalizar
    navigate(`/ficha/${ficha._id}`);
  };

  const renderStep = () => {
    const stepProps = {
      ficha,
      updateFicha,
      // Dados estáticos
      listaRacas, listaClasses, listaOrigens, listaTodasPericias,
      listaPoderes, listaDeuses,
      dadosRacas, dadosClasses, dadosOrigens, dadosHabilidadesClasse,
      dadosMagias, dadosHabilidades, dadosDeuses, dadosPoderesConcedidos,
      dadosHabilidadesRaciais,
      // Funções
      handleAtributoBaseChange,
      montarHabilidadesParaPanel,
      handleSaveEscolhas,
    };

    switch (currentStep) {
      case 0: return <StepConceito {...stepProps} />;
      case 1: return <StepAtributos {...stepProps} />;
      case 2: return <StepClasse {...stepProps} />;
      case 3: return <StepPericias {...stepProps} />;
      case 4: return <StepPoderes {...stepProps} />;
      case 5: return <StepMagias {...stepProps} />;
      case 6: return <StepRevisao {...stepProps} onFinish={handleFinish} />;
      default: return null;
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: '#1a1a1a',
      color: '#fff',
      padding: '20px'
    }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '30px',
        paddingBottom: '20px',
        borderBottom: '1px solid #333'
      }}>
        <button
          onClick={() => navigate('/')}
          style={{
            background: 'transparent',
            border: '1px solid #555',
            color: '#fff',
            padding: '8px 16px',
            borderRadius: '6px',
            cursor: 'pointer'
          }}
        >
          ← Voltar para Home
        </button>
        <h1 style={{ margin: 0, fontSize: '1.8rem', color: '#ffd700' }}>
          🧙‍♂️ Criador de Personagem
        </h1>
        <div style={{ width: '120px' }} />
      </div>

      {/* Stepper */}
      <WizardStepper steps={WIZARD_STEPS} currentStep={currentStep} />

      {/* Conteúdo do Step */}
      <div style={{
        maxWidth: '1200px',
        margin: '30px auto',
        background: '#2a2a2a',
        borderRadius: '12px',
        padding: '30px',
        minHeight: '400px'
      }}>
        {renderStep()}
      </div>

      {/* Botões de Navegação */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        maxWidth: '1200px',
        margin: '0 auto',
        paddingTop: '20px'
      }}>
        <button
          onClick={handleBack}
          disabled={currentStep === 0}
          style={{
            background: currentStep === 0 ? '#444' : '#666',
            color: '#fff',
            border: 'none',
            padding: '12px 30px',
            borderRadius: '8px',
            cursor: currentStep === 0 ? 'not-allowed' : 'pointer',
            fontSize: '1rem',
            fontWeight: 'bold'
          }}
        >
          ← Anterior
        </button>

        {currentStep === WIZARD_STEPS.length - 1 ? (
          <button
            onClick={handleFinish}
            style={{
              background: '#4caf50',
              color: '#fff',
              border: 'none',
              padding: '12px 30px',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '1rem',
              fontWeight: 'bold'
            }}
          >
            Finalizar Personagem ✓
          </button>
        ) : (
          <button
            onClick={handleNext}
            style={{
              background: '#2196f3',
              color: '#fff',
              border: 'none',
              padding: '12px 30px',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '1rem',
              fontWeight: 'bold'
            }}
          >
            Próximo →
          </button>
        )}
      </div>
    </div>
  );
}

export default Wizard;