import React, { useMemo } from 'react';
import ReactFlow, { Background, Controls, MiniMap } from 'reactflow';
import 'reactflow/dist/style.css';

// Nodos customizados para tener un diseño distinto si es crítico o promocionado
const FlightNodeComponent = ({ data }) => {
   const isCritical = data.is_critical;
   const isPromo = data.promocion;
   
   return (
      <div className={`p-3 rounded-lg border-2 shadow-lg min-w-[120px] transition-all
         ${isCritical ? 'bg-rose-950/80 border-rose-500 shadow-rose-500/30' : 'bg-sky-900/90 border-sky-400 shadow-sky-500/20'}
         ${isPromo && !isCritical ? 'border-amber-400 shadow-amber-500/20' : ''}
      `}>
         <div className="font-bold text-lg text-white text-center border-b border-white/20 pb-1 mb-2">
            {data.codigo}
         </div>
         <div className="space-y-1 text-xs text-sky-200">
            <div className="flex justify-between">
               <span>P. Final:</span>
               <span className="font-mono text-white">${data.precioFinal?.toFixed(1)}</span>
            </div>
            <div className="flex justify-between">
               <span>Balance:</span>
               <span className={`font-mono font-bold ${data.factor_balanceo > 1 || data.factor_balanceo < -1 ? 'text-rose-400' : 'text-emerald-400'}`}>
                  {data.factor_balanceo}
               </span>
            </div>
            <div className="flex justify-between">
               <span>Altura:</span>
               <span className="font-mono text-white">{data.altura}</span>
            </div>
         </div>
         {isCritical && <div className="mt-2 text-[10px] text-center bg-rose-500/20 text-rose-300 py-1 rounded">CRÍTICO</div>}
      </div>
   );
};

const nodeTypes = {
  flightNode: FlightNodeComponent,
};

// Convierte el nodo JSON anidado en Nodos (Nodes) y Arcos (Edges) para ReactFlow
const buildGraphData = (treeJson) => {
   const nodes = [];
   const edges = [];
   
   function traverse(node, x, y, level, parentId = null) {
      if (!node) return;
      
      const nodeId = node.codigo.toString();
      
      // Ajuste de "espacio" horizontal según la profundidad para evitar que se pisen (algo simple)
      const xOffset = 250 / Math.pow(1.5, level); 

      nodes.push({
         id: nodeId,
         type: 'flightNode',
         position: { x, y },
         data: node
      });
      
      if (parentId) {
         edges.push({
            id: `e-${parentId}-${nodeId}`,
            source: parentId,
            target: nodeId,
            type: 'smoothstep',
            animated: node.promocion // Animamos las aristas de los promos para un toque "vibrante"
         });
      }
      
      if (node.izquierdo) {
         traverse(node.izquierdo, x - xOffset, y + 150, level + 1, nodeId);
      }
      
      if (node.derecho) {
         traverse(node.derecho, x + xOffset, y + 150, level + 1, nodeId);
      }
   }
   
   traverse(treeJson, 400, 50, 1);
   
   return { nodes, edges };
}

export default function AVLTreeViz({ treeData }) {
   if (!treeData) return <div className="text-white">Sin datos para graficar...</div>;

   const { nodes, edges } = useMemo(() => buildGraphData(treeData), [treeData]);

   return (
      <div className="w-full h-full min-h-[500px]">
         <ReactFlow 
            nodes={nodes} 
            edges={edges}
            nodeTypes={nodeTypes}
            fitView
         >
            <Background color="#1e3a8a" gap={20} />
            <Controls />
            <MiniMap nodeStrokeColor="#0f172a" nodeColor="#3b82f6" maskColor="rgba(0,0,0,0.5)" />
         </ReactFlow>
      </div>
   );
}
