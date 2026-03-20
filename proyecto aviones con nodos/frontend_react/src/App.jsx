import { useState, useEffect, useRef } from 'react';
import { FiUpload, FiRefreshCw, FiZap, FiTrash2, FiActivity, FiCornerUpLeft } from 'react-icons/fi';
import api from './api';
import AVLTreeViz from './AVLTreeViz';

// Utilidad para extraer un reporte fácil de métricas (Estilo Mockup)
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

function App() {
  const [treeData, setTreeData] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [traversals, setTraversals] = useState(null);
  const [stressMode, setStressMode] = useState(false);
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

  const fileInputRef = useRef(null);

  const handleFileChange = async (event) => {
     const file = event.target.files[0];
     if (!file) return;

     setLoading(true);
     try {
        const text = await file.text();
        const jsonData = JSON.parse(text);
        
        await api.post('/load-tree', jsonData);
        await fetchTree();
     } catch(e) {
        alert("Error decodificando o enviando el JSON. Asegúrate de que el formato sea correcto.");
     } finally {
        setLoading(false);
        if (fileInputRef.current) fileInputRef.current.value = "";
     }
  };

  const handleLoadJsonClick = () => {
     fileInputRef.current?.click();
  };

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


   const handleCreateFlight = async () => {
      try {
         const prioridadMap = {
            BAJA: 1,
            MEDIA: 2,
            ALTA: 3
         };

      const payload = {
         codigo: formData.codigo,
         origen: formData.origen,
         destino: formData.destino || "N/A",
         horaSalida: formData.horaSalida || "00:00",

       // 🔥 IMPORTANTE
         precioBase: Number(formData.precioBase),
         pasajeros: Number(formData.pasajeros),
         prioridad: prioridadMap[formData.prioridad?.toUpperCase()] || 1,

         promocion: Boolean(formData.promocion),
         alerta: false
      };

      console.log("ENVIANDO:", payload); // 👈 DEBUG

      await api.post('/flights', payload);

      await fetchTree();

   } catch (e) {
      console.error(e.response?.data);
      alert(JSON.stringify(e.response?.data, null, 2));
   }
   };

  return (
    <div className="min-h-screen bg-[#f3f4f6] text-gray-800 font-sans flex flex-col p-2">
      
      {/* Top Menu (Estilo botonera plana de Windows viejo/Mockup) */}
      <div className="bg-[#1e293b] text-white p-2 flex flex-col items-center justify-center mb-2 shadow rounded">
         <div className="flex items-center gap-2 mb-1">
            <FiActivity className="text-gray-300" />
            <span className="font-semibold text-sm">SkyBalance</span>
         </div>
         <div className="flex gap-1 text-xs bg-gray-600 p-1 rounded">
             <button onClick={handleUndo} className="px-3 py-1 hover:bg-gray-500 rounded flex items-center gap-1 text-gray-200">
               <FiCornerUpLeft /> Deshacer
             </button>
             <div className="border-r border-gray-500 mx-1"></div>
             
             <input type="file" accept=".json" ref={fileInputRef} onChange={handleFileChange} className="hidden" />
             <span className="px-3 py-1 text-gray-400 cursor-not-allowed">Elegir archivo</span>
             <span className="px-1 py-1 text-gray-400">No se eligió ningún archivo</span>
             
             <button onClick={handleLoadJsonClick} disabled={loading} className="px-3 py-1 bg-gray-700 hover:bg-gray-500 rounded flex items-center gap-1 text-white shadow-sm border border-gray-500">
               <FiUpload /> {loading ? 'Cargando...' : 'Cargar JSON'}
             </button>
             
             <div className="border-r border-gray-500 mx-1"></div>
             <button onClick={toggleStress} className="px-3 py-1 hover:bg-gray-500 rounded flex items-center gap-1 text-gray-200">
               <FiZap /> Modo Estrés: {stressMode ? 'ON' : 'OFF'}
             </button>
         </div>
      </div>

      <div className="flex flex-1 gap-2 h-full overflow-hidden">
         {/* Sidebar Izquierdo: Formulario de Agregar Vuelo estilo Mockup */}
         <aside className="w-[300px] bg-white border border-gray-200 rounded shadow-sm flex flex-col p-4 overflow-y-auto">
            <h2 className="text-sm font-bold flex items-center gap-2 text-gray-800 border-b pb-2 mb-3">
              <span className="text-gray-500">✈</span> Datos del Vuelo
            </h2>
            <form className="space-y-3 text-xs" onSubmit={(e) => e.preventDefault()}>
               <div className="flex justify-between items-center gap-2">
                  <label className="text-gray-600 font-medium w-1/3">Código:</label>
                  <input
                  type="text"
                  value={formData.codigo}
                  onChange={(e) => setFormData({...formData, codigo: e.target.value})}
                  placeholder="001"
                  className="flex-1 p-1 border"
                  />               </div>
               <div className="flex justify-between items-center gap-2">
                  <label className="text-gray-600 font-medium w-1/3">Origen:</label>
                  <input
                    type="text"
                    value={formData.origen}
                    onChange={(e) => setFormData({...formData, origen: e.target.value})}
                    placeholder="Manizales"
                    className="flex-1 p-1 border border-gray-300 rounded shadow-sm focus:outline-none focus:border-gray-500"
                  />
               </div>
               <div className="flex justify-between items-center gap-2">
                  <label className="text-gray-600 font-medium w-1/3">Destino:</label>
                  <input
                    type="text"
                    value={formData.destino}
                    onChange={(e) => setFormData({...formData, destino: e.target.value})}
                    placeholder="ej: Bogotá"
                    className="flex-1 p-1 border border-gray-300 rounded shadow-sm focus:outline-none focus:border-gray-500"
                  />
               </div>
               <div className="flex justify-between items-center gap-2">
                  <label className="text-gray-600 font-medium w-1/3">Hora Salida:</label>
                  <input
                    type="text"
                    value={formData.hora_salida}
                    onChange={(e) => setFormData({...formData, hora_salida: e.target.value})}
                    placeholder="ej: 10:00"
                    className="flex-1 p-1 border border-gray-300 rounded shadow-sm focus:outline-none focus:border-gray-500"
                  />
               </div>
               <div className="flex justify-between items-center gap-2">
                  <label className="text-gray-600 font-medium w-1/3">Precio Base:</label>
                  <input
                    type="text"
                    value={formData.precio_base}
                    onChange={(e) => setFormData({...formData, precio_base: e.target.value})}
                    placeholder="ej: 350.00"
                    className="flex-1 p-1 border border-gray-300 rounded shadow-sm focus:outline-none focus:border-gray-500"
                  />
               </div>
               <div className="flex justify-between items-center gap-2">
                  <label className="text-gray-600 font-medium w-1/3">Pasajeros:</label>
                  <input
                    type="text"
                    value={formData.pasajeros}
                    onChange={(e) => setFormData({...formData, pasajeros: e.target.value})}
                    placeholder="ej: 120"
                    className="flex-1 p-1 border border-gray-300 rounded shadow-sm focus:outline-none focus:border-gray-500"
                  />
               </div>
               <div className="flex justify-between items-center gap-2">
                  <label className="text-gray-600 font-medium w-1/3">Prioridad:</label>
                  <input
                    type="text"
                    value={formData.prioridad}
                    onChange={(e) => setFormData({...formData, prioridad: e.target.value})}
                    placeholder="MEDIA"
                    className="flex-1 p-1 border border-gray-300 rounded shadow-sm focus:outline-none focus:border-gray-500"
                  />
               </div>
               <div className="flex justify-between items-center gap-2">
                  <label className="text-gray-600 font-medium w-1/3">Promoción:</label>
                  <input
                    type="text"
                    value={formData.promocion}
                    onChange={(e) => setFormData({...formData, promocion: e.target.value})}
                    placeholder="0"
                    className="flex-1 p-1 border border-gray-300 rounded shadow-sm focus:outline-none focus:border-gray-500"
                  />
               </div>
               
               <div className="flex justify-center gap-2 pt-4 border-t mt-4">
                  <button onClick={handleCreateFlight} className="px-4 py-1.5 bg-gray-100 hover:bg-gray-200 border border-gray-300 text-gray-700 rounded shadow-sm flex items-center font-medium">
                     <FiRefreshCw className="mr-1" /> Guardar
                  </button>
                  <button className="px-4 py-1.5 bg-gray-100 hover:bg-gray-200 border border-gray-300 text-gray-700 rounded shadow-sm flex items-center font-bold">
                     X Cancelar
                  </button>
               </div>
            </form>
         </aside>

         {/* Centro: Visualización del Arbol */}
         <section className="flex-1 bg-[#1e293b] rounded shadow relative flex flex-col">
            {treeData ? (
               <div className="flex-1 w-full h-[600px] min-h-[500px]">
                 <AVLTreeViz treeData={treeData} />
               </div>
            ) : (
               <div className="flex-1 flex flex-col items-center justify-center text-white/40">
                  <FiUpload className="text-4xl mx-auto mb-2 opacity-30" />
                  <p className="text-sm">Árbol Vacío</p>
               </div>
            )}
            
            {/* Consola inferior falsa estilo Mockup */}
            <div className="h-24 bg-[#0f172a] border-t-4 border-gray-600 p-2 text-xs font-mono text-gray-300 overflow-y-auto">
                <div>[Consola] Sistema SkyBalance AVL Iniciado</div>
                {treeData && <div>[Consola] Árbol renderizado satisfactoriamente. Nodos:{metrics?.nodes || '?'}</div>}
                {metrics?.massive_cancellations > 0 && <div className="text-rose-400">[Consola] ¡Se han registrado cancelaciones masivas!</div>}
                {stressMode && <div className="text-amber-400">[Alerta] Modo de Estrés Activo (Balanceo Detenido).</div>}
            </div>
         </section>
         
         {/* Sidebar Derecho: Métricas y Controles estilo Mockup */}
         <aside className="w-80 flex flex-col gap-2 overflow-y-auto">
            <MetricsPanel metrics={metrics} />
            <TraversalsPanel traversals={traversals} />
            
            <div className="bg-white border border-gray-200 p-4 rounded shadow-sm">
               <h3 className="text-sm font-bold flex items-center gap-2 text-gray-800 border-b pb-2 mb-3">
                 <FiTrash2 /> Negocio - Administrador
               </h3>
               <button onClick={handleOptimize} className="w-full py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 border border-gray-300 rounded text-xs shadow-sm flex items-center justify-center">
                  <FiTrash2 className="mr-1"/> Eliminar Menos Rentabilidad
               </button>
               {stressMode && (
                  <button onClick={async () => {
                        const res = await api.get('/tree/audit');
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
         </aside>

      </div>
    </div>
  );
}

export default App;
