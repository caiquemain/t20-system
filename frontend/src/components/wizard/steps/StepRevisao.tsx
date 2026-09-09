interface StepProps {
  ficha: any;
  onFinish: () => void;
}

export function StepRevisao({ ficha, onFinish }: StepProps) {
  return (
    <div>
      <h2 style={{ color: '#ffd700', marginBottom: '20px' }}>✅ Passo 7: Revisão Final</h2>
      <p style={{ color: '#aaa', marginBottom: '30px' }}>
        Revise seu personagem antes de começar a aventura!
      </p>

      <div style={{
        background: '#1a1a1a',
        border: '1px solid #555',
        borderRadius: '8px',
        padding: '20px',
        marginBottom: '20px'
      }}>
        <h3 style={{ color: '#fff', marginBottom: '15px' }}>📋 Resumo</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px', color: '#ccc' }}>
          <p><strong>Nome:</strong> {ficha.cabecalho.nome || '—'}</p>
          <p><strong>Raça:</strong> {ficha.cabecalho.raca || '—'}</p>
          <p><strong>Classe:</strong> {ficha.classes[0]?.nome || '—'}</p>
          <p><strong>Nível:</strong> {ficha.classes[0]?.nivel || 1}</p>
          <p><strong>Origem:</strong> {ficha.cabecalho.origem || '—'}</p>
          <p><strong>Divindade:</strong> {ficha.cabecalho.deus || 'Nenhuma'}</p>
        </div>
      </div>

      <button
        onClick={onFinish}
        style={{
          background: '#4caf50',
          color: '#fff',
          border: 'none',
          padding: '15px 40px',
          borderRadius: '8px',
          cursor: 'pointer',
          fontSize: '1.1rem',
          fontWeight: 'bold',
          width: '100%'
        }}
      >
        🎉 Finalizar Personagem
      </button>
    </div>
  );
}