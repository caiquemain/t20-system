import { T20Icon } from '../../T20Icon';

const FONT_BODY = "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif";

interface StepProps {
  ficha: any;
  onFinish: () => void;
}

export function StepRevisao({ ficha, onFinish }: StepProps) {
  const classe0 = ficha.classes?.[0];
  const classeLabel = classe0
    ? `${classe0.nome}${classe0.subclasse ? ` (${classe0.subclasse})` : ''}`
    : '—';

  const treinadas = Object.entries(ficha.pericias || {})
    .filter(([, p]: any) => (p?.treino || 0) > 0)
    .map(([nome, p]: any) => ({ nome, total: p?.total ?? 0 }));

  const habilidades = ficha.habilidades || [];
  const magias = ficha.combate?.magias || [];
  const attrs = [
    ['FOR', ficha.atributos?.forca ?? 0],
    ['DES', ficha.atributos?.destreza ?? 0],
    ['CON', ficha.atributos?.constituicao ?? 0],
    ['INT', ficha.atributos?.inteligencia ?? 0],
    ['SAB', ficha.atributos?.sabedoria ?? 0],
    ['CAR', ficha.atributos?.carisma ?? 0],
  ] as const;

  return (
    <div style={{ fontFamily: FONT_BODY, textTransform: 'none' }}>
      <h2 style={{ color: '#ffd700', marginBottom: 10, fontFamily: 'Tormenta, serif', display: 'inline-flex', alignItems: 'center', gap: 8 }}>
        <T20Icon name="check" size={22} /> Passo 7: Revisão Final
      </h2>
      <p style={{ color: '#94a3b8', marginBottom: 22, fontSize: '0.92rem' }}>
        Confira todos os números calculados do seu personagem antes de abrir a ficha completa!
      </p>

      {/* Identidade */}
      <div style={{ background: '#1a1d2e', border: '1px solid #32385a', borderRadius: 10, padding: 18, marginBottom: 16 }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 12, color: '#cbd5e1', fontSize: '0.92rem' }}>
          <div><span style={{ color: '#94a3b8' }}>Nome:</span> <strong>{ficha.cabecalho?.nome || '—'}</strong></div>
          <div><span style={{ color: '#94a3b8' }}>Raça:</span> <strong>{ficha.cabecalho?.raca || '—'}</strong></div>
          <div><span style={{ color: '#94a3b8' }}>Classe:</span> <strong>{classeLabel}</strong></div>
          <div><span style={{ color: '#94a3b8' }}>Nível:</span> <strong>{ficha.cabecalho?.nivel_total || 1}</strong></div>
          <div><span style={{ color: '#94a3b8' }}>Origem:</span> <strong>{ficha.cabecalho?.origem || 'Nenhuma'}</strong></div>
          <div><span style={{ color: '#94a3b8' }}>Divindade:</span> <strong style={{ color: '#ffd700' }}>{ficha.cabecalho?.deus || 'Nenhuma'}</strong></div>
        </div>
      </div>

      {/* Status + Atributos */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(110px, 1fr))', gap: 10, marginBottom: 16 }}>
        <StatBox label="PV Máx" value={ficha.status?.pv?.maximo ?? 0} color="#4caf50" />
        <StatBox label="PM Máx" value={ficha.status?.pm?.maximo ?? 0} color="#42a5f5" />
        <StatBox label="Defesa" value={ficha.status?.defesa?.total ?? 10} color="#ffd700" />
        <StatBox label="Desloc." value={`${ficha.status?.deslocamento ?? 9}m`} color="#e2e8f0" />
        <StatBox label="Carga Máx" value={ficha.inventario?.carga_maxima ?? 10} color="#cbd5e1" />
        {Number(ficha.combate?.circulo_maximo || 0) > 0 && (
          <StatBox label="CD Magias" value={ficha.combate?.cd_magias ?? 10} color="#ce93d8" />
        )}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: 8, marginBottom: 16 }}>
        {attrs.map(([sigla, val]) => (
          <div key={sigla} style={{ background: '#151828', border: '1px solid #2d3352', borderRadius: 8, padding: '10px 6px', textAlign: 'center' }}>
            <div style={{ fontSize: '0.7rem', color: '#94a3b8', fontWeight: 700 }}>{sigla}</div>
            <div style={{ fontSize: '1.25rem', fontWeight: 700, color: val >= 0 ? '#fff' : '#f87171' }}>
              {val > 0 ? `+${val}` : val}
            </div>
          </div>
        ))}
      </div>

      {/* Perícias, Habilidades e Magias */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 12, marginBottom: 22 }}>
        <div style={{ background: '#1a1d2e', border: '1px solid #32385a', borderRadius: 10, padding: 14 }}>
          <div style={{ fontSize: '0.78rem', color: '#ffd700', fontWeight: 700, textTransform: 'uppercase', marginBottom: 8 }}>
            Perícias Treinadas ({treinadas.length})
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
            {treinadas.map(t => (
              <span key={t.nome} style={{ fontSize: '0.78rem', padding: '3px 8px', borderRadius: 6, background: '#121524', border: '1px solid #32385a', color: '#e2e8f0' }}>
                {t.nome} <strong style={{ color: '#ffd700' }}>{t.total >= 0 ? `+${t.total}` : t.total}</strong>
              </span>
            ))}
            {treinadas.length === 0 && <span style={{ color: '#64748b', fontSize: '0.82rem' }}>Nenhuma treinada ainda.</span>}
          </div>
        </div>

        <div style={{ background: '#1a1d2e', border: '1px solid #32385a', borderRadius: 10, padding: 14 }}>
          <div style={{ fontSize: '0.78rem', color: '#ffd700', fontWeight: 700, textTransform: 'uppercase', marginBottom: 8 }}>
            Habilidades & Poderes ({habilidades.length})
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
            {habilidades.map((h: any, i: number) => (
              <span key={`${h.nome}-${i}`} style={{ fontSize: '0.78rem', padding: '3px 8px', borderRadius: 6, background: '#121524', border: '1px solid #32385a', color: '#cbd5e1' }}>
                {h.nome}
              </span>
            ))}
          </div>
        </div>

        {magias.length > 0 && (
          <div style={{ background: '#1a1d2e', border: '1px solid #32385a', borderRadius: 10, padding: 14 }}>
            <div style={{ fontSize: '0.78rem', color: '#ce93d8', fontWeight: 700, textTransform: 'uppercase', marginBottom: 8 }}>
              Magias Conhecidas ({magias.length})
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
              {magias.map((m: any) => (
                <span key={m.nome} style={{ fontSize: '0.78rem', padding: '3px 8px', borderRadius: 6, background: 'rgba(156,39,176,0.14)', border: '1px solid rgba(206,147,216,0.4)', color: '#e9d5ff' }}>
                  {m.nome} ({m.circulo}º)
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      <button
        onClick={onFinish}
        style={{
          background: '#4caf50',
          color: '#fff',
          border: 'none',
          padding: '15px 40px',
          borderRadius: 8,
          cursor: 'pointer',
          fontSize: '1.1rem',
          fontWeight: 'bold',
          width: '100%',
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 8,
        }}
      >
        <T20Icon name="check" size={20} /> Finalizar Personagem e Abrir Ficha
      </button>
    </div>
  );
}

function StatBox({ label, value, color }: { label: string; value: string | number; color: string }) {
  return (
    <div style={{ background: '#1a1d2e', border: '1px solid #32385a', borderRadius: 8, padding: '10px 12px', textAlign: 'center' }}>
      <div style={{ fontSize: '0.7rem', color: '#94a3b8', textTransform: 'uppercase' }}>{label}</div>
      <div style={{ fontSize: '1.3rem', fontWeight: 700, color }}>{value}</div>
    </div>
  );
}