import React, { useMemo } from 'react';
import ReactFlow, { Background, Controls, MiniMap, Handle, Position } from 'reactflow';
import 'reactflow/dist/style.css';

const FlightNodeComponent = ({ data }) => {
   const isCritical = data.alerta || data.is_critical; 
   const isPromo = data.promocion; 
   
   let bgColor = 'bg-[#4caf50]'; // Verde nativo del ejemplo
   if (isCritical) bgColor = 'bg-[#ff9800]'; // Naranja
   else if (isPromo) bgColor = 'bg-[#9c27b0]'; // Morado

   return (
      <div className={`px-4 py-2 shadow-lg border-2 border-transparent hover:border-white text-white min-w-[90px] text-center transition-colors cursor-pointer ${bgColor}`}>
         <Handle type="target" position={Position.Top} className="opacity-0" />
         
         <div className="font-bold text-[15px] tracking-wide flex justify-center items-center h-5">
            {data.codigo}
         </div>
         <div className="text-[10px] opacity-90 leading-tight">
            BF: {data.factor_balanceo > 0 ? `+${data.factor_balanceo}` : data.factor_balanceo}
         </div>
         
         <Handle type="source" position={Position.Bottom} className="opacity-0" />
      </div>
   );
};

const nodeTypes = {
  flightNode: FlightNodeComponent,
};

const getTreeDepth = (node) => {
   if (!node) return 0;
   return 1 + Math.max(getTreeDepth(node.izquierdo), getTreeDepth(node.derecho));
}

const buildGraphData = (treeJson) => {
   const nodes = [];
   const edges = [];
   const maxDepth = getTreeDepth(treeJson);
   
   const baseHorizontalSpacing = Math.pow(1.8, maxDepth) * 35; // Calibrado
   const layerHeight = 120; // Más corto como en el ejemplo

   function traverse(node, x, y, level, parentId = null) {
      if (!node) return;
      
      const nodeId = node.codigo.toString();
      
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
            type: 'straight', // Líneas rectas idénticas al mockup
            style: { strokeWidth: 1.5, stroke: '#d1d5db' },
         });
      }
      
      const dynamicXOffset = baseHorizontalSpacing / Math.pow(2, level);
      
      if (node.izquierdo) {
         traverse(node.izquierdo, x - dynamicXOffset, y + layerHeight, level + 1, nodeId);
      }
      if (node.derecho) {
         traverse(node.derecho, x + dynamicXOffset, y + layerHeight, level + 1, nodeId);
      }
   }
   
   traverse(treeJson, 0, 50, 1);
   return { nodes, edges };
}

export default function AVLTreeViz({ treeData, onNodeClick }) {
   if (!treeData) return null;

   const { nodes, edges } = useMemo(() => buildGraphData(treeData), [treeData]);

   return (
      <div style={{ width: '100%', height: '100%', minHeight: '500px', flex: 1 }}>
         <ReactFlow 
            nodes={nodes} 
            edges={edges}
            nodeTypes={nodeTypes}
            onNodeClick={(event, node) => onNodeClick && onNodeClick(node.data)}
            fitView
         >
            {/* Fondo oscuro para igualar el pantallazo */}
            <Background color="#333" gap={16} /> 
            <Controls />
            <MiniMap nodeStrokeColor="#000" nodeColor="#4caf50" maskColor="rgba(0,0,0,0.5)" />
         </ReactFlow>
      </div>
   );
}
