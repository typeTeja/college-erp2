export type NodeType = 'ROOT' | 'YEAR' | 'PROGRAM' | 'REGULATION' | 'BATCH' | 'SEMESTER' | 'SECTION_GROUP' | 'LAB_GROUP' | 'SECTION' | 'LAB';

export interface StructureNode {
    id: string; // Unique composition key (e.g., "year_2024_prog_1")
    type: NodeType;
    label: string;
    data?: any; // The actual entity (AcademicYear, Program, Batch, etc.)
    children?: StructureNode[]; // For pre-loaded children
    hasChildren?: boolean; // To show expand icon even if children not loaded
    details?: any; // Extra metadata for badges (e.g., student count)
}

export interface TreeContextState {
    expandedNodes: Set<string>;
    selectedNodeId: string | null;
    toggleExpand: (nodeId: string) => void;
    selectNode: (node: StructureNode) => void;
}
