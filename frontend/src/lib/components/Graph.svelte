<script lang="ts">
	import * as d3 from 'd3';
	import type { Graph } from '../models'; // Adjust import as needed

	interface Props {
		width: number;
		height: number;
		data: Graph;
	}

	const { width, height, data }: Props = $props();

	const MARGIN = { top: 60, right: 60, bottom: 60, left: 60 };

	let boundsWidth: number = $derived(width - MARGIN.right - MARGIN.left);
	let boundsHeight: number = $derived(height - MARGIN.top - MARGIN.bottom);

	let dendrogramGenerator = $derived(d3.cluster<Graph>().size([boundsHeight, boundsWidth]));

	let hierarchy: d3.HierarchyNode<Graph> = $state(d3.hierarchy(data).sum((d: Graph) => d.value));
	let dendrogram: d3.HierarchyPointNode<Graph> = $derived(dendrogramGenerator(hierarchy));

	const horizontalLinkGenerator = d3
		.linkHorizontal()
		.x((d: any) => d[0])
		.y((d: any) => d[1]);
</script>

<div>
	<svg {width} {height}>
		<g
			width={boundsWidth}
			height={boundsHeight}
			transform={`translate(${MARGIN.left},${MARGIN.top})`}
		>
			{#if dendrogram}
				{#each dendrogram.descendants() as node (node.data.id)}
					<g>
						<circle cx={node.y} cy={node.x} r={5} stroke="transparent" fill="#69b3a2" />
						<text
							x={node.y + 15}
							y={node.x}
							font-size="12"
							text-anchor="top"
							alignment-baseline="middle"
							fill="white"
						>
							{node.data.name}
						</text>
					</g>
				{/each}
				{#each dendrogram.descendants() as node (node.data.id)}
					{#if node.parent}
						<path
							fill="none"
							stroke="grey"
							d={horizontalLinkGenerator({
								source: [node.parent.y, node.parent.x],
								target: [node.y, node.x]
							})}
						/>
					{/if}
				{/each}
			{/if}
		</g>
	</svg>
</div>
