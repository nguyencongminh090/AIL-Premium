---
name: knowledge-graph
description: Extracts a knowledge graph from an academic paper — typed entities (methods, models, datasets, metrics, concepts, tasks, components, prior-work baselines) and the typed relations between them — as an explicit triples table plus a Mermaid graph, and merges them into a cumulative project-wide graph so cross-paper links (shared datasets, metrics, lineage) emerge. Use for: knowledge graph of 003, build a KG, extract entities and relations, đồ thị tri thức, trích xuất thực thể quan hệ, map the concepts. Output is Vietnamese (terms preserved) to notes/<id>-kg.md, with the master graph at notes/knowledge-graph.md.
argument-hint: <paper id | filename | path | all>
---

# Knowledge Graph Worker

This skill turns a paper into a structured knowledge graph: typed entities and the
typed relations among them, expressed both as machine-readable triples and as a
Mermaid diagram. It also accumulates a project-wide master graph so connections
across papers become visible.

## Conventions
This skill treats `.claude/rules/research-conventions.md` as binding for input
resolution, Vietnamese-with-preserved-terms labels, `notes/` location, and fidelity.
It never invents entities or relations that the paper does not support.

## Entity & relation types
- **Entity types:** Method, Model, Dataset, Metric, Concept, Task, Problem,
  Component, PriorWork.
- **Relation types:** proposes, addresses, uses, part-of, based-on, evaluated-on,
  measured-by, improves-over, compared-with, trained-on.

## Procedure
1. **Resolve the target** from `$ARGUMENTS` per the shared rules; if empty, it asks.
   For `all`, it processes each paper and merges them all into the master graph.
2. **Read the PDF.**
3. **Extract entities**, each tagged with its type and the source paper id.
4. **Extract relations** as triples `(subject) —relation→ (object)`, grounded in the
   text.
5. **Emit per paper:** a triples table and a `flowchart LR` Mermaid graph with a
   `classDef` per entity type and labeled edges.
6. **Merge into the master** at `notes/knowledge-graph.md`: it reads the existing
   master (if any), adds new entities/relations, de-duplicates entities shared with
   other papers (same dataset/metric/concept) so cross-paper edges form, and tags
   each node/edge with its source paper id(s). If no master exists, it creates one.
7. **Glossary, save, preview** — writes `notes/<id>-kg.md`, updates the master, and
   prints the saved paths plus a count of entities/relations added.

## Output template (`notes/<id>-kg.md`)
````
# Đồ thị tri thức — <id> · <Title>
> Nguồn: <filename> · Worker: knowledge-graph · Ngày: <YYYY-MM-DD>

## Thực thể (Entities)
| Thực thể (Entity) | Loại (Type) | Ghi chú |

## Quan hệ (Triples)
| Subject | Relation | Object |

## Sơ đồ (Mermaid)
```mermaid
flowchart LR
  classDef method fill:#e8f0fe;
  classDef dataset fill:#fce8e6;
  %% nodes & edges...
```

## Thuật ngữ (Glossary)
````
