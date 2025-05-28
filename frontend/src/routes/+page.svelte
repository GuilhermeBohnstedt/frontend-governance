<script lang="ts">
	import Dendrogram from '$lib/components/Graph.svelte';
	import { data } from '$lib/utils/d3/data';

	let modal: HTMLDialogElement;
	let windowHeight: number = $state(0);
	let windowWidth: number = $state(0);
</script>

<button class="btn btn-primary fixed right-5 top-3 z-40" onclick={() => modal?.showModal()}>
	Open Modal
</button>

<svelte:window bind:innerHeight={windowHeight} bind:innerWidth={windowWidth} />

{#if windowHeight === 0 || windowWidth === 0}
	<p>Loading...</p>
{:else}
	<Dendrogram {data} height={windowHeight} width={windowWidth} />
{/if}

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
