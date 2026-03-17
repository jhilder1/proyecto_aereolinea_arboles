import { useState, useEffect } from 'react';
import { FiUpload, FiRefreshCw, FiZap, FiTrash2, FiActivity, FiCornerUpLeft } from 'react-icons/fi';
import api from './api';
import AVLTreeViz from './AVLTreeViz';

// Utilidad para extraer un reporte fácil de métricas
function MetricsPanel({ metrics }) {
  if (!metrics) return null;
  return (
    <div className="bg-white/5 border border-white/10 p-4 rounded-xl backdrop-blur-md shadow-lg w-full">
      <h3 className="text-xl font-bold flex items-center gap-2 mb-4 text-sky-400">
        <FiActivity />
        Métricas del Sistema
      </h3>
      <div className="grid grid-cols-2 gap-4">
         <div className="bg-sky-950/50 p-3 rounded-lg">
            <span className="text-xs text-sky-300 font-semibold uppercase">Altura AVL</span>
            <p className="text-2xl font-bold text-white">{metrics.height}</p>
         </div>
         <div className="bg-sky-950/50 p-3 rounded-lg">
            <span className="text-xs text-sky-300 font-semibold uppercase">Hojas</span>
            <p className="text-2xl font-bold text-white">{metrics.leaves}</p>
         </div>
         <div className="bg-sky-950/50 p-3 rounded-lg col-span-2">
            <span className="text-xs text-rose-300 font-semibold uppercase">Cancelaciones Masivas</span>
            <p className="text-2xl font-bold text-white">{metrics.massive_cancellations}</p>
         </div>
         
         <div className="col-span-2 mt-2">
            <span className="text-xs text-sky-300 font-semibold uppercase mb-2 block">Rotaciones Históricas</span>
            <div className="grid grid-cols-4 gap-2 text-center text-sm font-mono">
              <div className="bg-sky-900/40 p-1 rounded">LL: {metrics.rotations.single_left || 0}</div>
              <div className="bg-sky-900/40 p-1 rounded">RR: {metrics.rotations.single_right || 0}</div>
              <div className="bg-sky-900/40 p-1 rounded">LR: {metrics.rotations.double_left || 0}</div>
              <div className="bg-sky-900/40 p-1 rounded">RL: {metrics.rotations.double_right || 0}</div>
            </div>
         </div>
      </div>
    </div>
  )
}

function TraversalsPanel({ traversals }) {
  if (!traversals) return null;
  return (
    <div className="bg-white/5 border border-white/10 p-4 rounded-xl backdrop-blur-md shadow-lg w-full mt-4">
      <h3 className="text-sm font-bold flex items-center gap-2 mb-3 text-emerald-400">
        Recorridos del Árbol
      </h3>
      <div className="space-y-3 font-mono text-xs">
         <div>
            <span className="text-emerald-300/70">InOrder: </span>
            <div className="bg-black/20 p-2 rounded mt-1 overflow-x-auto whitespace-nowrap scrollbar-hide">
               {traversals.in_order?.join(" → ") || "Vacío"}
            </div>
         </div>
         <div>
            <span className="text-emerald-300/70">PreOrder: </span>
            <div className="bg-black/20 p-2 rounded mt-1 overflow-x-auto whitespace-nowrap scrollbar-hide">
               {traversals.pre_order?.join(" → ") || "Vacío"}
            </div>
         </div>
         <div>
            <span className="text-emerald-300/70">PostOrder: </span>
            <div className="bg-black/20 p-2 rounded mt-1 overflow-x-auto whitespace-nowrap scrollbar-hide">
               {traversals.post_order?.join(" → ") || "Vacío"}
            </div>
         </div>
      </div>
    </div>
  )
}

function App() {
  const [treeData, setTreeData] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [traversals, setTraversals] = useState(null);
  const [stressMode, setStressMode] = useState(false);
  const [loading, setLoading] = useState(false);

  // Cargar estado inicial
  const fetchTree = async () => {
    try {
      const res = await api.get('/tree');
      setTreeData(res.data.avl);
      setMetrics(res.data.metrics);
      setTraversals(res.data.traversals);
      setStressMode(res.data.stress_mode);
    } catch (error) {
       console.error("Error fetching tree", error);
    }
  };

  useEffect(() => {
    fetchTree();
  }, []);

  const handleLoadJson = async () => {
     setLoading(true);
     try {
        await api.post('/load-tree');
        await fetchTree();
     } catch(e) {
        alert("Error cargando JSON o seleccion cancelada.");
     } finally {
        setLoading(false);
     }
  }

  const toggleStress = async () => {
     try {
         await api.post('/mode', {
            stress_mode: !stressMode,
            depth_threshold: 5
         });
         await fetchTree();
     } catch(e) {
         alert("Error cambiando modo");
     }
  }

  const handleOptimize = async () => {
      try {
          const res = await api.delete('/flights/optimize/economic');
          alert(res.data.message);
          await fetchTree();
      } catch(e) {
         alert("Error optimizando");
      }
  }

  const handleUndo = async () => {
      try {
          const res = await api.post('/history/undo');
          if(res.data.undo){
              await fetchTree();
          } else {
              alert("Nada que deshacer");
          }
      } catch(e) {
         alert("Error deshaciendo");
      }
  }

  return (
    <div className="min-h-screen bg-sky-900 text-slate-200 flex flex-col">
      {/* Navbar Premium */}
      <nav className="border-b border-white/10 bg-sky-950/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-sky-400 to-blue-600 rounded-xl flex place-items-center justify-center shadow-lg shadow-sky-500/20">
                 <FiActivity className="text-white text-xl" />
              </div>
              <span className="font-bold text-2xl tracking-tight text-white bg-clip-text text-transparent bg-gradient-to-r from-white to-sky-200">
                SkyBalance
              </span>
            </div>
            <div className="flex gap-3">
               <button 
                  onClick={handleUndo}
                  className="px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 transition flex items-center gap-2 font-medium border border-white/10"
               >
                 <FiCornerUpLeft />
                 Deshacer
               </button>
               <button 
                  onClick={handleLoadJson} disabled={loading}
                  className="px-4 py-2 rounded-lg bg-sky-600 hover:bg-sky-500 transition flex items-center gap-2 font-medium"
               >
                 <FiUpload />
                 {loading ? 'Cargando...' : 'Cargar JSON'}
               </button>
               <button 
                  onClick={toggleStress}
                  className={`px-4 py-2 rounded-lg transition flex items-center gap-2 font-medium shadow-lg
                     ${stressMode ? 'bg-rose-500 hover:bg-rose-600 shadow-rose-500/20 text-white' : 'bg-amber-500 hover:bg-amber-600 shadow-amber-500/20 text-white'}`}
               >
                 <FiZap />
                 Modo Estrés: {stressMode ? 'ON' : 'OFF'}
               </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Area Principal */}
      <main className="max-w-[1400px] w-full mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-4 gap-8 flex-1">
         {/* Sidebar izq (Metricas y Controles) */}
         <aside className="lg:col-span-1 space-y-6 flex flex-col">
            <MetricsPanel metrics={metrics} />
            <TraversalsPanel traversals={traversals} />

            <div className="bg-white/5 border border-white/10 p-4 rounded-xl backdrop-blur-md">
               <h3 className="text-lg font-bold mb-4 flex items-center gap-2 text-rose-400">
                 <FiTrash2 /> Administrador
               </h3>
               <button 
                  onClick={handleOptimize}
                  className="w-full py-2 mb-2 bg-rose-500/20 hover:bg-rose-500/40 text-rose-300 border border-rose-500/30 rounded-lg transition text-sm"
               >
                  <FiTrash2 className="inline mr-2"/> Menor Rentabilidad
               </button>
               {stressMode && (
                  <button 
                     onClick={async () => {
                        const res = await api.get('/tree/audit');
                        alert("Estado Auditoría: " + res.data.status + "\n" + JSON.stringify(res.data.inconsistencies));
                     }}
                     className="w-full py-2 bg-amber-500/20 hover:bg-amber-500/40 text-amber-300 border border-amber-500/30 rounded-lg transition text-sm"
                  >
                     <FiZap className="inline mr-2"/> Auditoría AVL
                  </button>
               )}
            </div>

            <div className="bg-white/5 border border-white/10 p-4 rounded-xl backdrop-blur-md">
               <h3 className="text-lg font-bold mb-4 flex items-center gap-2 text-sky-400">
                 <FiRefreshCw /> Simulación Cola
               </h3>
                <button 
                  onClick={async () => {
                        try {
                           const flightData = {
                                codigo: "FL-" + Math.floor(Math.random() * 9000 + 1000),
                                origen: "NUEVO",
                                precioBase: Math.floor(Math.random() * 500 + 100),
                                pasajeros: Math.floor(Math.random() * 200 + 50)
                           };
                           const res = await api.post('/flights/enqueue', flightData);
                           alert("Vuelo Encolado. Cola actual: " + res.data.queue_size);
                        } catch(e) {}
                  }}
                  className="w-full py-2 mb-2 bg-sky-500/20 hover:bg-sky-500/40 text-sky-300 border border-sky-500/30 rounded-lg transition text-sm"
               >
                  + Encolar Vuelo
               </button>
               <button 
                  onClick={async () => {
                        const res = await api.post('/flights/process');
                        if(res.data.processed) await fetchTree();
                        alert(res.data.message);
                  }}
                  className="w-full py-2 bg-emerald-500/20 hover:bg-emerald-500/40 text-emerald-300 border border-emerald-500/30 rounded-lg transition text-sm"
               >
                  Procesar Siguiente Vuelo
               </button>
            </div>
         </aside>

         {/* Visualización */}
         <section className="lg:col-span-3 bg-white/5 border border-white/10 rounded-xl overflow-hidden shadow-2xl relative min-h-[600px] flex items-center justify-center">
            {treeData ? (
               <AVLTreeViz treeData={treeData} />
            ) : (
               <div className="text-center text-white/40">
                  <FiUpload className="text-6xl mx-auto mb-4 opacity-50" />
                  <p className="text-xl font-medium">No hay datos cargados</p>
                  <p className="text-sm mt-2">Usa "Cargar JSON" para iniciar el sistema.</p>
               </div>
            )}
         </section>
      </main>
    </div>
  );
}

export default App;
