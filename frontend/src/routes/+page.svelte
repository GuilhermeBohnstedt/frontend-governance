<script lang="ts">
	import Graph from '$lib/components/Graph.svelte';
	import { nodes } from '$lib/utils/d3/data';

	const packageJson = {
		name: 'frontend',
		private: false,
		version: '0.0.1',
		type: 'module',
		packageManager: 'pnpm@10.11.0'
	};

	let modal: HTMLDialogElement;
	let windowHeight: number;
	let windowWidth: number;
</script>

<button class="btn btn-primary fixed right-5 top-3 z-40" onclick={() => modal?.showModal()}>
	Open Modal
</button>

<svelte:window bind:innerHeight={windowHeight} bind:innerWidth={windowWidth} />

<Graph data={nodes} height={windowHeight} width={windowWidth} />

<dialog bind:this={modal} id="form-modal" class="modal z-50">
	<div class="modal-box">
		<h3 class="text-lg font-bold">Hello!</h3>
		<p class="py-4">Press ESC key or click the button below to close</p>
		<div class="modal-action">
			<button class="btn" onclick={() => modal?.close()}>Close</button>
		</div>
	</div>
</dialog>

<style>
</style>
