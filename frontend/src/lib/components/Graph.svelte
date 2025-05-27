<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import * as d3 from 'd3';
	import type { GraphNode } from '$lib/models';

	interface Props {
		data: GraphNode[];
		width: number;
		height: number;
	}

	const { data, width, height}: Props = $props();

	let container: HTMLDivElement;

	let svgEl: SVGSVGElement | null = null;
	let timeout: ReturnType<typeof setTimeout>;

	function diagonal(d: any) {
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

	function render() {
		container.innerHTML = '';

		const svg = d3
			.create('svg')
			.attr('width', width)
			.attr('height', height)
			.attr('viewBox', [0, 0, width, height])
			.attr('style', 'max-width: 100%; height: auto; height: intrinsic;');

		const g = svg.append('g').attr('transform', 'translate(40,0)');

		const tree = d3.tree().size([height - 400, width - 160]);
		const cluster = d3.cluster().size([height, width - 160]);

		const stratify = d3.stratify().parentId((d: any) => {
			return d.id.substring(0, d.id.lastIndexOf('.'));
		});

		const root = stratify(data).sort(function (a: any, b: any) {
			return a.height - b.height || a.id.localeCompare(b.id);
		});

		cluster(root);

		const link = g
			.selectAll('.link')
			.data(root.descendants().slice(1))
			.enter()
			.append('path')
			.attr('class', 'link')
			.attr('d', diagonal);

		timeout = setTimeout(function () {
			d3.select(container)
				.select('input[value="tree"]')
				.property('checked', true)
				.dispatch('change');
		}, 1000);

		const changed = function (this: d3.BaseType) {
			clearTimeout(timeout);
			const input = this as HTMLInputElement;
			if (input && input.value === 'tree') {
				tree(root);
			} else {
				cluster(root);
			}
			const t = d3.transition().duration(750);
			node.transition(t).attr('transform', function (d: any) {
				return 'translate(' + d.y + ',' + d.x + ')';
			});
			link.transition(t).attr('d', diagonal);
		};

		const node = g
			.selectAll('.node')
			.data(root.descendants())
			.enter()
			.append('g')
			.attr('class', function (d: any) {
				return 'node' + (d.children ? ' node--internal' : ' node--leaf');
			})
			.attr('transform', function (d: any) {
				return 'translate(' + d.y + ',' + d.x + ')';
			});

		node.append('circle').attr('r', 2.5);

		node
			.append('text')
			.attr('dy', 3)
			.attr('x', function (d: any) {
				return d.children ? -8 : 8;
			})
			.style('text-anchor', function (d: any) {
				return d.children ? 'end' : 'start';
			})
			.text(function (d: any) {
				return d.id.substring(d.id.lastIndexOf('.') + 1);
			});

		d3.select(container).selectAll('input').on('change', changed);

		svgEl = svg.node();
		if (svgEl) container.appendChild(svgEl);
	}

	onMount(() => {
		render();
	});

	onDestroy(() => {
		if (timeout) clearTimeout(timeout);
	});

	$effect(() => {
		if (data && data.length) {
			render();
		}
	});
</script>

<div bind:this={container} class="d3-fullscreen">
	<form style="position:absolute;left:10px;top:10px;">
		<label><input type="radio" name="mode" value="cluster" checked /> Dendrogram</label>
		<label><input type="radio" name="mode" value="tree" /> Tree</label>
	</form>
</div>

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
