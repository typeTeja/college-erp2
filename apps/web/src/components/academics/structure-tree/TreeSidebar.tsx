"use client";

import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '@/utils/api';
import { TreeNode } from './TreeNode';
import { StructureNode, NodeType } from './types';
import { Skeleton } from '@/components/ui/skeleton';

interface TreeSidebarProps {
    selectedNodeId: string | null;
    onSelectNode: (node: StructureNode) => void;
}

export function TreeSidebar({ selectedNodeId, onSelectNode }: TreeSidebarProps) {
    const [expanded, setExpanded] = useState<Set<string>>(new Set());

    // Root Query: Academic Years
    const { data: years = [], isLoading: isLoadingYears } = useQuery({
        queryKey: ['academic-years'],
        queryFn: async () => {
            const res = await api.get('/academic/academic-years');
            return res.data;
        }
    });

    // Helper to toggle expansion
    const toggleExpand = (nodeId: string) => {
        const newExpanded = new Set(expanded);
        if (newExpanded.has(nodeId)) {
            newExpanded.delete(nodeId);
        } else {
            newExpanded.add(nodeId);
        }
        setExpanded(newExpanded);
    };

    if (isLoadingYears) {
        return <div className="space-y-2 p-2">
            {[1, 2, 3].map(i => <Skeleton key={i} className="h-8 w-full" />)}
        </div>;
    }

    return (
        <div className="select-none">
            {years.map((year: any) => (
                <RecursiveNode
                    key={`year_${year.id}`}
                    node={{
                        id: `year_${year.id}`,
                        type: 'YEAR',
                        label: year.year,
                        data: year,
                        hasChildren: true
                    }}
                    level={0}
                    expanded={expanded}
                    selectedId={selectedNodeId}
                    onToggle={toggleExpand}
                    onSelect={onSelectNode}
                />
            ))}
        </div>
    );
}

// Recursive Component for Lazy Loading Children
interface RecursiveNodeProps {
    node: StructureNode;
    level: number;
    expanded: Set<string>;
    selectedId: string | null;
    onToggle: (id: string) => void;
    onSelect: (node: StructureNode) => void;
}

function RecursiveNode({ node, level, expanded, selectedId, onToggle, onSelect }: RecursiveNodeProps) {
    const isExpanded = expanded.has(node.id);
    
    // Determine query key based on node type and hierarchy
    // We compose the ID to contain lineage: "year_1_prog_5_reg_2" for safer fetching context?
    // Actually simplicity: Pass parent data in `node.data` context or reconstruct.
    // The node.data contains the entity. We need parent context for filtering below.
    // Let's rely on constructing queries based on node.type and node.data.id

    const shouldFetch = isExpanded && (!node.children || node.children.length === 0);
    
    // Dynamic Query Dispatcher
    const { data: children, isLoading } = useQuery({
        queryKey: ['tree-children', node.id, node.type],
        queryFn: async () => fetchChildren(node),
        enabled: shouldFetch,
        staleTime: 5 * 60 * 1000 // 5 mins cache
    });

    const displayChildren = children || node.children || [];

    return (
        <div>
            <TreeNode
                node={node}
                level={level}
                isExpanded={isExpanded}
                isSelected={selectedId === node.id}
                onToggle={() => onToggle(node.id)}
                onSelect={() => onSelect(node)}
                isLoading={isLoading}
            />
            
            {isExpanded && (
                <div className="flex flex-col">
                    {displayChildren.map((child: StructureNode) => (
                        <RecursiveNode
                            key={child.id}
                            node={child}
                            level={level + 1}
                            expanded={expanded}
                            selectedId={selectedId}
                            onToggle={onToggle}
                            onSelect={onSelect}
                        />
                    ))}
                    {!isLoading && displayChildren.length === 0 && (
                        <div className="py-1 px-4 text-xs text-slate-400 italic" style={{ paddingLeft: `${(level + 1) * 16 + 8}px` }}>
                            (Empty)
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

// ---------------------------------------------------------------------------
// 🧠 Tree Logic: The Graph Resolver
// ---------------------------------------------------------------------------

async function fetchChildren(parent: StructureNode): Promise<StructureNode[]> {
    switch (parent.type) {
        
        // 1. YEAR -> PROGRAMS
        case 'YEAR': {
            // Fetch all active programs.
            // In a real advanced mode, we'd only filter programs valid for this year.
            const res = await api.get('/academic/programs');
            const programs = res.data;
            
            return programs.map((prog: any) => ({
                id: `${parent.id}_prog_${prog.id}`, // year_X_prog_Y
                type: 'PROGRAM',
                label: prog.name, // or prog.code
                data: { ...prog, parentYearId: parent.data.id }, // Carry context
                hasChildren: true
            }));
        }

        // 2. PROGRAM -> REGULATIONS
        case 'PROGRAM': {
            // Fetch regulations for this program
            const progId = parent.data.id;
            const res = await api.get('/academic/regulations'); // This returns all, need filtering
            // Note: Ideally API supports ?program_id=X. Assuming client filter for now based on existing API.
            const allRegs = res.data;
            const programRegs = allRegs.filter((r: any) => r.program_id === progId);

            return programRegs.map((reg: any) => ({
                id: `${parent.id}_reg_${reg.id}`,
                type: 'REGULATION',
                label: reg.name,
                data: { ...reg, parentYearId: parent.data.parentYearId, parentProgId: progId },
                hasChildren: true
            }));
        }

        // 3. REGULATION -> BATCHES (The Crucial Link)
        case 'REGULATION': {
            // Find batches for this Regulation AND the root Year (Admission Year)
            // Context: parentYearId comes from lineage
            const regId = parent.data.id;
            const yearId = parent.data.parentYearId;
            const progId = parent.data.parentProgId;

            // Fetch batches (ideally filtered)
            const res = await api.get(`/academic/batches?program_id=${progId}`);
            // Filter client side for safety
            const batches = res.data.filter((b: any) => 
                b.regulation_id === regId && 
                b.admission_year_id === yearId
            );

            return batches.map((batch: any) => ({
                id: `${parent.id}_batch_${batch.id}`,
                type: 'BATCH',
                label: batch.batch_name,
                data: batch,
                hasChildren: true
            }));
        }

        // 4. BATCH -> SEMESTERS
        case 'BATCH': {
            const batchId = parent.data.id;
            const res = await api.get(`/academic/batch-semesters?batch_id=${batchId}`);
            const semesters = res.data.sort((a: any, b: any) => a.semester_number - b.semester_number);

            return semesters.map((sem: any) => ({
                id: `${parent.id}_sem_${sem.id}`,
                type: 'SEMESTER',
                label: `Semester ${sem.semester_number}`,
                data: sem,
                hasChildren: true // Has Sections + Labs
            }));
        }

        // 5. SEMESTER -> SECTIONS + LABS
        case 'SEMESTER': {
            const semId = parent.data.id;
            
            // Parallel fetch
            const [secRes, labRes] = await Promise.all([
                api.get(`/academic/sections?batch_semester_id=${semId}`),
                api.get(`/academic/practical-batches?batch_semester_id=${semId}`)
            ]);

            const sections = secRes.data;
            const labs = labRes.data;

            const children: StructureNode[] = [];

            // Group: Theory Sections
            if (sections.length > 0) {
                 children.push({
                    id: `${parent.id}_group_theory`,
                    type: 'SECTION_GROUP',
                    label: 'Sections (Theory)',
                    children: sections.map((sec: any) => ({
                        id: `${parent.id}_sec_${sec.id}`,
                        type: 'SECTION',
                        label: sec.name, // "Section A"
                        data: sec,
                        details: { count: sec.current_strength }
                    })),
                    // We directly provide children here, ignoring async
                    hasChildren: false // It's a group, we expanded it immediately or treat as leaf with visible children?
                    // Better: Just return the children nodes directly? The design asked for hierarchy.
                    // Design: Semester -> Sections (Theory) -> Section A
                 });
            }

             // Group: Labs
            if (labs.length > 0) {
                children.push({
                   id: `${parent.id}_group_labs`,
                   type: 'LAB_GROUP',
                   label: 'Lab Batches (Practical)',
                   children: labs.map((lab: any) => ({
                       id: `${parent.id}_lab_${lab.id}`,
                       type: 'LAB',
                       label: lab.name,
                       data: lab,
                       details: { count: lab.current_strength }
                   })),
                   hasChildren: false
                });
            }
            
            // NOTE: The RecursiveNode component expects `children` to be fetched. 
            // If we return nodes that ALREADY have `children` property populated, 
            // the RecursiveNode logic needs to handle that. 
            // My RecursiveNode implementation uses `displayChildren = children || node.children`.
            // So if I return a "SECTION_GROUP" node with pre-populated children, 
            // passing it to RecursiveNode will work IF `expanded` is handled.
            // But wait, the SECTION_GROUP node itself needs to be expandable? 
            // If I want them to be expandable, I should return them as expandable nodes 
            // and have a Case 'SECTION_GROUP' that returns the cached children.
            // OR simpler: Just attach the children property and set hasChildren=true. 
            // But `hasChildren` normally triggers a fetch.
            
            // HACK for V1: Flat list under semester?
            // "Semester"
            //   - "Section A"
            //   - "Lab 1"
            
            // Design Requirement: "Semester -> Sections (THEORY) -> Section A"
            // So we DO need intermediate groups.
            
            // Let's modify the return structure.
            // We return SECTION_GROUP node.
            // If we put data in `node.children`, `RecursiveNode` will use it naturally if `shouldFetch` is false.
            // `shouldFetch` is `isExpanded && (!node.children || node.children.length === 0)`
            // So if we populate `children`, it won't fetch. Perfect.
            
            return children;
        }

        default:
            return [];
    }
}
