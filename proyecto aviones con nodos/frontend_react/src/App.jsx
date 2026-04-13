import { useState, useEffect, useRef } from 'react';
import { FiUpload, FiRefreshCw, FiZap, FiTrash2, FiActivity, FiCornerUpLeft, FiClock, FiPlus, FiFolder } from 'react-icons/fi';
import api from './api';
import AVLTreeViz from './AVLTreeViz';
import axios from 'axios';

function MetricsPanel({ metrics }) {
  if (!metrics) return null;
  return (
    <div className="bg-white border border-gray-200 p-4 rounded shadow-sm w-full text-center">
      <h3 className="text-sm font-bold flex items-center justify-center gap-2 mb-3 text-gray-800 border-b pb-2">
        <FiActivity />
        Métricas del Sistema
      </h3>
      
      <div className="space-y-2 text-sm text-gray-600">
         <div>
            <span className="block font-semibold">Altura AVL</span>
            <p className="font-mono">{metrics.height}</p>
         </div>
         <div>
            <span className="block font-semibold">Hojas</span>
            <p className="font-mono">{metrics.leaves}</p>
         </div>
         <div>
            <span className="block font-semibold">Cancelaciones Masivas</span>
            <p className="font-mono">{metrics.massive_cancellations}</p>
         </div>
         
         <div className="pt-2 border-t text-xs">
            <span className="block font-semibold mb-1">Rotaciones Históricas</span>
            <div className="space-y-1">
               <p>LL: {metrics.rotations.single_left || 0}</p>
               <p>RR: {metrics.rotations.single_right || 0}</p>
               <p>LR: {metrics.rotations.double_left || 0}</p>
               <p>RL: {metrics.rotations.double_right || 0}</p>
            </div>
         </div>
      </div>
    </div>
  )
}

function TraversalsPanel({ traversals }) {
  if (!traversals) return null;
  return (
    <div className="bg-white border border-gray-200 p-4 rounded shadow-sm w-full mt-2">
      <h3 className="text-sm font-bold text-gray-800 mb-2">Recorridos del Árbol</h3>
      <div className="space-y-2 font-mono text-xs text-gray-700">
         <div>
            <span className="font-semibold">InOrder: </span>
            <div className="bg-gray-50 p-1 border rounded mt-1 overflow-x-auto whitespace-nowrap scrollbar-hide">
               {traversals.in_order?.join(" → ") || "Vacío"}
            </div>
         </div>
         <div>
            <span className="font-semibold">PreOrder: </span>
            <div className="bg-gray-50 p-1 border rounded mt-1 overflow-x-auto whitespace-nowrap scrollbar-hide">
               {traversals.pre_order?.join(" → ") || "Vacío"}
            </div>
         </div>
         <div>
            <span className="font-semibold">PostOrder: </span>
            <div className="bg-gray-50 p-1 border rounded mt-1 overflow-x-auto whitespace-nowrap scrollbar-hide">
               {traversals.post_order?.join(" → ") || "Vacío"}
            </div>
         </div>
      </div>
    </div>
  )
}

function HistoryPanel({ timeline, onTimeTravel }) {
  if (!timeline) return null;
  return (
    <div className="bg-white border border-gray-200 p-4 rounded shadow-sm w-full mt-2 flex flex-col h-64">
      <h3 className="text-sm font-bold text-gray-800 mb-2 flex items-center gap-1 border-b pb-2">
         <FiClock /> Historial de Movimientos
      </h3>
      <div className="flex-1 space-y-1 text-xs overflow-y-auto pr-1">
         {timeline.slice().reverse().map((event) => (
             <div 
                key={event.index} 
                onClick={() => onTimeTravel(event.index)} 
                className="p-1.5 border border-transparent hover:border-blue-300 hover:bg-blue-50 cursor-pointer rounded flex justify-between items-center transition-colors shadow-sm bg-gray-50 mb-1"
             >
                <div className="flex items-center gap-2">
                    <span className="text-[10px] font-bold text-gray-500 w-4">{event.index}.</span>
                    <span className="font-semibold text-gray-700">{event.action}</span>
                </div>
                <span className="text-[9px] text-gray-400">
                    {new Date(event.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: "2-digit", second: "2-digit" })}
                </span>
             </div>
         ))}
         {timeline.length === 0 && <div className="text-gray-400 p-2">Sin historial</div>}
      </div>
    </div>
  )
}

function WelcomeScreen({ onEnter }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-br from-[#0f172a] via-[#1e293b] to-[#0f172a] text-white overflow-hidden">
       {/* Background decorative elements */}
       <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-blue-500/20 rounded-full blur-[100px]"></div>
       <div className="absolute bottom-[-10%] right-[-10%] w-96 h-96 bg-purple-500/20 rounded-full blur-[100px]"></div>

       <div className="relative p-10 bg-white/10 backdrop-blur-lg border border-white/20 shadow-2xl rounded-3xl flex flex-col items-center text-center max-w-lg mx-4">
          <div className="w-24 h-24 mb-6 bg-gradient-to-tr from-blue-500 to-purple-600 rounded-2xl rotate-3 flex items-center justify-center shadow-[0_0_40px_rgba(59,130,246,0.6)] transition-transform hover:rotate-6 hover:scale-105 duration-300">
             <FiActivity className="text-5xl text-white" />
          </div>
          
          <h1 className="text-5xl font-extrabold tracking-tight mb-2 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-300 to-white">
              SkyBalance
          </h1>
          <h2 className="text-xs font-bold text-blue-300/80 tracking-[0.3em] uppercase mb-8">Administrador Dinámico de Vuelos</h2>
          
          <p className="text-gray-300 text-sm mb-10 leading-relaxed font-light">
             Bienvenido a la plataforma avanzada de SkyBalance. Modela rutas, analiza rentabilidad concurrente con umbrales críticos y viaja a través del historial temporal apoyado en <strong className="text-white font-medium">Árboles AVL</strong>.
          </p>
          
          <button 
             onClick={onEnter}
             className="group relative px-8 py-3.5 font-semibold text-white transition-all duration-300 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full hover:from-blue-500 hover:to-purple-500 hover:shadow-[0_0_30px_rgba(168,85,247,0.5)] focus:outline-none transform hover:-translate-y-1"
          >
             <span className="relative flex items-center gap-2 text-sm tracking-wide uppercase">
                Ingresar al Sistema <FiZap className="group-hover:animate-pulse text-lg" />
             </span>
          </button>
       </div>
    </div>
  );
}

function App() {
  const [hasEntered, setHasEntered] = useState(false);
  const [activeTreeId, setActiveTreeId] = useState("Principal");
  const [treesList, setTreesList] = useState(["Principal"]);

  const [treeData, setTreeData] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [traversals, setTraversals] = useState(null);
  const [stressMode, setStressMode] = useState(false);
  const [criticalDepth, setCriticalDepth] = useState(3);
  const [timeline, setTimeline] = useState([]);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
      codigo: '',
      origen: '',
      destino: '',
      horaSalida: '',
      precioBase: '',
      pasajeros: '',
      prioridad: '',
      promocion: false,
      alerta: false
   });

  const fetchTree = async () => {
    try {
      const res = await api.get(`/tree?tree_id=${activeTreeId}`);
      setTreeData(res.data.avl);
      setMetrics(res.data.metrics);
      setTraversals(res.data.traversals);
      setStressMode(res.data.stress_mode);
      setCriticalDepth(res.data.critical_depth_threshold);
      const histRes = await api.get(`/history/${activeTreeId}/timeline`);
      setTimeline(histRes.data.timeline);
      
      const sessRes = await api.get(`/trees`);
      setTreesList(sessRes.data.trees);
    } catch (error) {
       console.error("Error fetching tree", error);
    }
  };

  useEffect(() => {
    fetchTree();
  }, [activeTreeId]);

  const fileInputRef = useRef(null);

  const handleFileChange = async (event) => {
     const file = event.target.files[0];
     if (!file) return;

     setLoading(true);
     try {
        const text = await file.text();
        const jsonData = JSON.parse(text);
        
        await api.post(`/load-tree?tree_id=${activeTreeId}`, jsonData);
        await fetchTree();
     } catch(e) {
        alert("Error decodificando o enviando el JSON.");
     } finally {
        setLoading(false);
        if (fileInputRef.current) fileInputRef.current.value = "";
     }
  };

  const handleCreateNewTree = async () => {
      const name = prompt("Ingresa un nombre para el nuevo vuelo/árbol:");
      if(name && name.trim()){
          await api.post(`/trees/${name.trim()}`);
          setActiveTreeId(name.trim());
      }
  };

  const handleTimeTravel = async (index) => {
      try {
          await api.post(`/history/${activeTreeId}/travel/${index}`);
          await fetchTree();
      } catch (e) {
          alert("Error viajando temporalmente");
      }
  };

  const toggleStress = async () => {
     try {
         await api.post(`/mode?tree_id=${activeTreeId}`, {
            stress_mode: !stressMode,
            depth_threshold: criticalDepth
         });
         await fetchTree();
     } catch(e) {
         alert("Error cambiando modo");
     }
  }

  const updateCriticalDepth = async () => {
      try {
         await api.post(`/depth?tree_id=${activeTreeId}`, {
            depth_threshold: criticalDepth
         });

         await fetchTree();

      } catch(e) {
         alert("Error actualizando profundidad crítica");
      }
   };

  const handleOptimize = async () => {
      try {
          const res = await api.delete(`/flights/optimize/economic?tree_id=${activeTreeId}`);
          alert(res.data.message);
          await fetchTree();
      } catch(e) {
         alert("Error optimizando");
      }
  }

  const handleUndo = async () => {
      try {
          const res = await api.post(`/history/undo?tree_id=${activeTreeId}`);
          if(res.data.undo){
              await fetchTree();
          } else {
              alert("Nada que deshacer");
          }
      } catch(e) {
         alert("Error deshaciendo");
      }
  }

   const handleDelete = async (codigo) => {
       try {
          await api.delete(`/flights/${codigo}?cascade=true&tree_id=${activeTreeId}`);
          await fetchTree();
          setSelectedNode(null);
       } catch (error) {
          alert("Error eliminando nodo");
       }
   };

   const handleCreateFlight = async () => {
      try {
         const prioridadMap = {
            BAJA: 1, MEDIA: 2, ALTA: 3
         };

         const payload = {
            codigo: formData.codigo,
            origen: formData.origen,
            destino: formData.destino || "N/A",
            horaSalida: formData.horaSalida || "00:00",
            precioBase: Number(formData.precioBase),
            pasajeros: Number(formData.pasajeros),
            prioridad: prioridadMap[formData.prioridad?.toUpperCase()] || 1,
            promocion: Boolean(formData.promocion),
            alerta: false
         };

         await api.post(`/flights?tree_id=${activeTreeId}`, payload);
         await fetchTree();

      }catch (e) {
         console.error("ERROR", e);
      }
   };

   const handleExportTree = async () => {
      try {
         const response = await axios.get(`http://localhost:8000/api/export?tree_id=${activeTreeId}`)
         const blob = new Blob([JSON.stringify(response.data, null, 2)], { type: "application/json" })
         const url = window.URL.createObjectURL(blob)
         const link = document.createElement("a")
         link.href = url
         link.download = `arbol_avl_${activeTreeId}.json`
         document.body.appendChild(link)
         link.click()
         document.body.removeChild(link)
      } catch (error) {
         console.error("Error exportando", error)
      }
   }

   const [selectedNode, setSelectedNode] = useState(null);

   const handleNodeClick = (nodeData) => {
      setSelectedNode(nodeData);
   };

   const [comparison, setComparison] = useState(null)

   const handleCompare = async () => {
      try {
         const response = await axios.get(`http://localhost:8000/api/compare?tree_id=${activeTreeId}`)
         setComparison(response.data)
      } catch (error) {
         console.error("Error comparando", error)
      }
   }

  if (!hasEntered) {
    return <WelcomeScreen onEnter={() => setHasEntered(true)} />;
  }

  return (
    <div className="min-h-screen bg-[#f3f4f6] text-gray-800 font-sans flex flex-col p-2">
      
      {/* Top Menu */}
      <div className="bg-[#1e293b] text-white p-2 flex flex-col items-center justify-center mb-2 shadow rounded">
         <div className="flex items-center gap-4 mb-2 w-full justify-between px-4">
             <div className="flex items-center gap-2">
                <FiActivity className="text-gray-300" />
                <span className="font-semibold text-sm">SkyBalance</span>
             </div>
             
             {/* Workspace Selector */}
             <div className="flex items-center gap-2">
                <FiFolder className="text-gray-400" />
                <select 
                    value={activeTreeId}
                    onChange={(e) => setActiveTreeId(e.target.value)}
                    className="bg-gray-700 text-white text-xs p-1 rounded border border-gray-600 outline-none"
                >
                    {treesList.map(t => <option key={t} value={t}>{t}</option>)}
                </select>
                <button onClick={handleCreateNewTree} className="p-1 hover:bg-gray-600 rounded bg-gray-700 border border-gray-600">
                    <FiPlus />
                </button>
             </div>
         </div>

         <div className="flex gap-1 text-xs bg-gray-600 p-1 rounded">
             <button onClick={handleUndo} className="px-3 py-1 hover:bg-gray-500 rounded flex items-center gap-1 text-gray-200">
               <FiCornerUpLeft /> Deshacer
             </button>
             <div className="border-r border-gray-500 mx-1"></div>
             
             <input type="file" accept=".json" ref={fileInputRef} onChange={handleFileChange} className="hidden" />
             <span className="px-3 py-1 text-gray-400 cursor-not-allowed">Elegir archivo</span>
             
             <button onClick={() => fileInputRef.current?.click()} disabled={loading} className="px-3 py-1 bg-gray-700 hover:bg-gray-500 rounded flex items-center gap-1 text-white shadow-sm border border-gray-500">
               <FiUpload /> {loading ? 'Cargando...' : 'Cargar JSON'}
             </button>

             <button onClick={handleExportTree} disabled={loading} className="px-3 py-1 bg-gray-700 hover:bg-gray-500 rounded flex items-center gap-1 text-white shadow-sm border border-gray-500">
               <FiUpload /> {loading ? 'Cargando...' : 'Guardar JSON'}
             </button>
             
             <div className="border-r border-gray-500 mx-1"></div>
             <button onClick={toggleStress} className="px-3 py-1 hover:bg-gray-500 rounded flex items-center gap-1 text-gray-200">
               <FiZap /> Modo Estrés: {stressMode ? 'ON' : 'OFF'}
             </button>
             
         </div>
      </div>

      <div className="flex flex-1 gap-2 h-full overflow-hidden">
         {/* Sidebar Izquierdo */}
         <aside className="w-[300px] bg-white border border-gray-200 rounded shadow-sm flex flex-col p-4 overflow-y-auto">
            <h2 className="text-sm font-bold flex items-center gap-2 text-gray-800 border-b pb-2 mb-3">
              <span className="text-gray-500">✈</span> Datos del Vuelo
            </h2>
            <form className="space-y-3 text-xs" onSubmit={(e) => e.preventDefault()}>
               <div className="flex justify-between items-center gap-2">
                  <label className="text-gray-600 font-medium w-1/3">Código:</label>
                  <input type="text" value={formData.codigo} onChange={(e) => setFormData({...formData, codigo: e.target.value})} placeholder="001" className="flex-1 p-1 border"/>
               </div>
               <div className="flex justify-between items-center gap-2">
                  <label className="text-gray-600 font-medium w-1/3">Origen:</label>
                  <input type="text" value={formData.origen} onChange={(e) => setFormData({...formData, origen: e.target.value})} placeholder="Manizales" className="flex-1 p-1 border rounded" />
               </div>
               <div className="flex justify-between items-center gap-2">
                  <label className="text-gray-600 font-medium w-1/3">Destino:</label>
                  <input type="text" value={formData.destino} onChange={(e) => setFormData({...formData, destino: e.target.value})} placeholder="Bogotá" className="flex-1 p-1 border rounded" />
               </div>
               <div className="flex justify-between items-center gap-2">
                  <label className="text-gray-600 font-medium w-1/3">Base P.:</label>
                  <input type="text" value={formData.precioBase} onChange={(e) => setFormData({...formData, precioBase: e.target.value})} placeholder="350.00" className="flex-1 p-1 border rounded" />
               </div>
               <div className="flex justify-between items-center gap-2">
                  <label className="text-gray-600 font-medium w-1/3">Pasajeros:</label>
                  <input type="text" value={formData.pasajeros} onChange={(e) => setFormData({...formData, pasajeros: e.target.value})} placeholder="120" className="flex-1 p-1 border rounded" />
               </div>
               
               <div className="flex justify-center gap-2 pt-4 border-t mt-4">
                  <button onClick={handleCreateFlight} className="px-4 py-1.5 bg-gray-100 hover:bg-gray-200 border border-gray-300 text-gray-700 rounded shadow-sm flex items-center font-medium">
                     <FiRefreshCw className="mr-1" /> Guardar
                  </button>
                  <button onClick={handleCompare} disabled={loading} className="px-3 py-1 bg-gray-700 hover:bg-gray-500 rounded flex items-center gap-1 text-white shadow-sm border border-gray-500">
                     <FiUpload /> Comparar
                  </button>
               </div>
            </form>

            <HistoryPanel timeline={timeline} onTimeTravel={handleTimeTravel} />

         </aside>

         {/* Centro */}
         <section className="flex-1 bg-[#1e293b] rounded shadow relative flex flex-col overflow-hidden">
            <div className="flex-1 w-full h-full relative" style={{ minHeight: '600px' }}>
                {treeData ? (
                    <div className="absolute inset-0">
                    <AVLTreeViz 
                        treeData={treeData}
                        onNodeClick={handleNodeClick}
                    />           
                    </div>
                ) : (
                <div className="flex-1 flex flex-col items-center justify-center text-white/40 h-full">
                    <FiUpload className="text-4xl mx-auto mb-2 opacity-30" />
                    <p className="text-sm">Árbol Secundario Vacío</p>
                </div>
                )}
            </div>
            
            <div className="h-24 min-h-[96px] bg-[#0f172a] border-t-4 border-gray-600 p-2 text-xs font-mono text-gray-300 overflow-y-auto">
                <div>[Consola] SkyBalance - Vuelo: {activeTreeId}</div>
                {stressMode && <div className="text-amber-400">[Alerta] Modo de Estrés Activo.</div>}
            </div>
         </section>
         
         {/* Sidebar Derecho */}
         <aside className="w-80 flex flex-col gap-2 overflow-y-auto pr-1">
            <MetricsPanel metrics={metrics} />
            <TraversalsPanel traversals={traversals} />

            {selectedNode && (
               <div className="bg-white border border-gray-200 p-4 rounded shadow-sm">
                  <h3 className="text-sm font-bold text-gray-800 border-b pb-2 mb-2">Nodo Seleccionado</h3>
                  <div className="text-xs text-gray-600 mb-2">Código: {selectedNode.codigo}</div>
                  <button
                     onClick={() => handleDelete(selectedNode.codigo)}
                     className="w-full py-1.5 bg-red-100 hover:bg-red-200 text-red-700 border border-red-300 rounded text-xs shadow-sm"
                  >
                     Eliminar Vuelo
                  </button>
               </div>
            )}
            
            <div className="bg-white border border-gray-200 p-4 rounded shadow-sm">
               <h3 className="text-sm font-bold flex items-center gap-2 text-gray-800 border-b pb-2 mb-3">
                 <FiTrash2 /> Negocio - Administrador
               </h3>
               <button onClick={handleOptimize} className="w-full py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 border border-gray-300 rounded text-xs shadow-sm flex items-center justify-center">
                  <FiTrash2 className="mr-1"/> Eliminar Menos Rentabilidad
               </button>
               {stressMode && (
                  <button onClick={async () => {
                        const res = await api.get(`/tree/audit?tree_id=${activeTreeId}`);
                        alert("Auditoría: " + res.data.status + "\n" + JSON.stringify(res.data.inconsistencies));
                     }}
                     className="w-full py-1.5 mt-2 bg-amber-50 hover:bg-amber-100 text-amber-700 border border-amber-300 rounded text-xs shadow-sm"
                  >
                     <FiZap className="inline mr-1"/> Auditar Árbol
                  </button>
               )}
            </div>

               

             <div className="bg-white border border-gray-200 p-4 rounded shadow-sm">
               <h3 className="text-sm font-bold flex items-center gap-2 text-gray-800 border-b pb-2 mb-3">
                 <FiRefreshCw /> Simulación Cola
               </h3>
               <button onClick={async () => {
                        try {
                           const flightData = {
                                codigo: "SB-" + Math.floor(Math.random() * 900 + 100),
                                origen: "NUEVO",
                                precioBase: Math.floor(Math.random() * 500 + 100),
                                pasajeros: Math.floor(Math.random() * 200 + 50)
                           };
                           const res = await api.post('/flights/enqueue', flightData);
                           alert("Encolado. Fila: " + res.data.queue_size);
                        } catch(e) {}
                  }}
                  className="w-full py-1.5 mb-2 bg-gray-100 hover:bg-gray-200 text-gray-700 border border-gray-300 rounded text-xs shadow-sm"
               >
                  Agregar Vuelo Falso a Cola
               </button>
               <button onClick={async () => {
                        const res = await api.post('/flights/process');
                        if(res.data.processed) await fetchTree();
                        alert(res.data.message);
                  }}
                  className="w-full py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 border border-gray-300 rounded text-xs shadow-sm font-bold"
               >
                  Correr Procesador
               </button>
            </div>
            <div className="bg-white border border-gray-200 p-4 rounded shadow-sm">
               <h3 className="text-sm font-bold flex items-center gap-2 text-gray-800 border-b pb-2 mb-3">
                  <FiZap /> Configuración Estrés
               </h3>

               <div className="text-xs text-gray-600 mb-2">
                  Profundidad Crítica
               </div>

               <input
                  type="number"
                  min="0"
                  value={criticalDepth}
                  onChange={(e) => setCriticalDepth(parseInt(e.target.value))}
                  className="w-full p-1 border border-gray-300 rounded text-xs mb-2"
               />

               <button
                  onClick={updateCriticalDepth}
                  className="w-full py-1.5 bg-amber-50 hover:bg-amber-100 text-amber-700 border border-amber-300 rounded text-xs shadow-sm"
               >
                  Aplicar Profundidad
               </button>

               {stressMode && (
                  <div className="text-[10px] text-amber-600 mt-2">
                     Penalización 25% aplicada a nodos bajo esta profundidad
                  </div>
               )}
            </div>
            
            {comparison && (
            <div className="bg-white border border-gray-200 p-4 rounded shadow-sm">
               <h3 className="text-sm font-bold text-gray-800 border-b pb-2 mb-2">
                  Comparación AVL vs BST
               </h3>
               <div className="text-xs text-gray-600">
                  <div className="mb-2">
                     <strong>AVL</strong>
                     <div>Raíz: {comparison.AVL.root}</div>
                     <div>Altura: {comparison.AVL.height}</div>
                     <div>Hojas: {comparison.AVL.leaves}</div>
                  </div>
                  <div className="border-t pt-2">
                     <strong>BST</strong>
                     <div>Raíz: {comparison.BST.root}</div>
                     <div>Altura: {comparison.BST.height}</div>
                     <div>Hojas: {comparison.BST.leaves}</div>
                  </div>
               </div>
            </div>
          )}

         </aside>
      </div>
    </div>
  );
}

export default App;
