<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import * as d3 from 'd3';
	import type { GraphNode } from '$lib/models';

	interface Props {
		data: GraphNode[];
		width: number;
		height: number;
	}

	const { data, width, height }: Props = $props();

	let container: HTMLDivElement;

	let svgEl: SVGSVGElement | null = null;

	let hierarchyRoot: any = null;

	function diagonal(d: any): string {
		return (
			'M' +
			d.y +
			',' +
			d.x +
			'C' +
			(d.parent.y + 100) +
			',' +
			d.x +
			' ' +
			(d.parent.y + 100) +
			',' +
			d.parent.x +
			' ' +
			d.parent.y +
			',' +
			d.parent.x
		);
	}

	// Helper to build a hierarchical structure with collapse state
	function buildHierarchy(data: GraphNode[]) {
		const stratify = d3.stratify().parentId((d: any) => {
			return d.id.substring(0, d.id.lastIndexOf('.'));
		});
		const root = stratify(data).sort(function (a: any, b: any) {
			return a.height - b.height || a.id.localeCompare(b.id);
		});
		root.each((d: any) => {
			d._children = d.children; // Save original children
			if (d.collapsed === undefined) d.collapsed = true;
		});
		return root;
	}

	let prevPositions: Record<string, { x: number; y: number }> = {};
	let lastToggledNodeId: string | null = null;

	function isDescendantOrSelf(node: any, ancestorId: string | null): boolean {
		if (!ancestorId) return false;
		let current = node;
		while (current) {
			if (current.id === ancestorId) return true;
			current = current.parent;
		}
		return false;
	}

	// Collapse or expand node
	function toggleCollapse(d: any) {
		lastToggledNodeId = d.id;
		if (d.collapsed) {
			d.children = d._children;
			d.collapsed = false;
		} else {
			d.children = null;
			d.collapsed = true;
		}
		render();
	}

	function render() {
		container.innerHTML = ''; // Clear previous content
		if (!hierarchyRoot) return; // Exit if no data

		const svg = d3
			.create('svg')
			.attr('width', width)
			.attr('height', height)
			.attr('viewBox', [-10, 0, width, height])
			.attr('style', 'max-width: 100%; height: auto; height: intrinsic;');

		const g = svg.append('g').attr('transform', 'translate(40,0)');
		const cluster = d3.cluster().size([height, width - 160]);

		// Collapse nodes that are marked as collapsed
		hierarchyRoot.each((d: any) => {
			if (d.collapsed && d.children) {
				d._children = d.children;
				d.children = null;
			} else if (!d.collapsed && !d.children && d._children) {
				d.children = d._children;
			}
		});

		cluster(hierarchyRoot);

		// Save current positions for animation
		const nodes = hierarchyRoot.descendants();
		nodes.forEach((d: any) => {
			if (!prevPositions[d.id]) {
				prevPositions[d.id] = { x: d.x, y: d.y };
			}
		});

		const transitionDuration = 600;
		const transitionEase = d3.easeCubicInOut;

		// --- Links with selective animation ---
		const link = g.selectAll('.link')
			.data(nodes.slice(1), (d: any) => d.id);

		const linkEnter = link.enter()
			.append('path')
			.attr('class', 'link')
			.attr('style', 'fill:none; stroke: #ffff; stroke-width: 1.5px;stroke-opacity: 0.4;')
			.attr('d', (d: any) => {
				const p = prevPositions[d.id] || d;
				const o = { x: p.x, y: p.y, parent: { x: p.x, y: p.y } };
				return diagonal(o);
			});

		linkEnter.merge(link as any)
			.each(function(d: any) {
				const sel = d3.select(this);
				if (isDescendantOrSelf(d, lastToggledNodeId)) {
					sel.transition()
						.duration(transitionDuration)
						.ease(transitionEase)
						.attr('d', diagonal);
				} else {
					sel.attr('d', diagonal);
				}
			});

		link.exit()
			.each(function(d: any) {
				const sel = d3.select(this);
				if (isDescendantOrSelf(d, lastToggledNodeId)) {
					const p = prevPositions[d.id] || d;
					const o = { x: p.x, y: p.y, parent: { x: p.x, y: p.y } };
					sel.transition()
						.duration(transitionDuration)
						.ease(transitionEase)
						.attr('d', diagonal(o))
						.remove();
				} else {
					sel.remove();
				}
			});

		// --- Nodes with selective animation ---
		const node = g.selectAll('.node')
			.data(nodes, (d: any) => d.id);

		const nodeEnter = node.enter()
			.append('g')
			.attr('class', 'node')
			.attr('color', (d: any) => d.children ? '#999' : '#ffff')
			.attr('transform', (d: any) => {
				const p = prevPositions[d.id] || d;
				return `translate(${p.y},${p.x})`;
			})
			.style('cursor', 'pointer')
			.on('click', function (event: MouseEvent, d: any) {
				event.stopPropagation();
				toggleCollapse(d);
			});

		nodeEnter.append('circle')
			.attr('r', 6)
			.attr('fill', (d: any) => d._children ? '#ffff' : '#999')
			.attr('stroke', '#333')
			.attr('stroke-width', 1.5);

		nodeEnter.append('text')
			.attr('fill', '#ffff')
			.attr('font-size', 10)
			.attr('font-family', 'sans-serif')
			.attr('text-shadow', (d: any) =>
				d.children
					? '0 1px 0 #000000, 0 -1px 0 #000000, 1px 0 0 #000000, -1px 0 0 #000000'
					: ''
			)
			.attr('dy', 3)
			.attr('x', (d: any) => (d.children || d._children ? -12 : 8))
			.style('text-anchor', (d: any) => (d.children || d._children ? 'end' : 'start'))
			.text((d: any) => d.id.substring(d.id.lastIndexOf('.') + 1));

		nodeEnter.filter((d: any) => d._children)
			.append('text')
			.attr('x', -18)
			.attr('dy', 3)
			.attr('fill', '#ffff')
			.attr('font-size', 14)
			.text((d: any) => d.collapsed ? '+' : '-');

		nodeEnter.merge(node as any)
			.each(function(d: any) {
				const sel = d3.select(this);
				if (isDescendantOrSelf(d, lastToggledNodeId)) {
					sel.transition()
						.duration(transitionDuration)
						.ease(transitionEase)
						.attr('transform', `translate(${d.y},${d.x})`);
				} else {
					sel.attr('transform', `translate(${d.y},${d.x})`);
				}
			});

		node.exit()
			.each(function(d: any) {
				const sel = d3.select(this);
				const p = prevPositions[d.id] || d;
				if (isDescendantOrSelf(d, lastToggledNodeId)) {
					sel.transition()
						.duration(transitionDuration)
						.ease(transitionEase)
						.attr('transform', `translate(${p.y},${p.x})`)
						.remove();
				} else {
					sel.remove();
				}
			});

		// Update prevPositions for next animation
		nodes.forEach((d: any) => {
			prevPositions[d.id] = { x: d.x, y: d.y };
		});

		svgEl = svg.node();
		if (svgEl) container.appendChild(svgEl);

		// Reset after render so next click animates only its subtree
		lastToggledNodeId = null;
	}

	onMount(() => {
		if (data && data.length) {
			hierarchyRoot = buildHierarchy(data);
			render();
		}
	});

	$effect(() => {
		if (data && data.length) {
			hierarchyRoot = buildHierarchy(data);
			render();
		}
	});
</script>

<div bind:this={container} class="d3-fullscreen"></div>

<style>
	.d3-fullscreen {
		position: fixed;
		inset: 0;
		width: 100vw;
		height: 100vh;
		z-index: 10;
		background: rgb(107, 107, 107);
	}
</style>
