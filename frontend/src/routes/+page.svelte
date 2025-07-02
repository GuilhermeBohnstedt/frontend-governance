<script lang="ts">
	import Form from '$lib/components/Form.svelte';
	import Dendrogram from '$lib/components/Graph.svelte';
	import Table from '$lib/components/Table.svelte';
	import type { PackageJson, PackageResult } from '$lib/models';
	import { data } from '$lib/utils/d3/data';

	let modal: HTMLDialogElement;
	let windowHeight: number = $state(0);
	let windowWidth: number = $state(0);

	let dataLoaded = $state<PackageResult[]>([]);
</script>

<button class="btn btn-primary fixed right-5 top-3 z-40" onclick={() => modal?.showModal()}>
	Open Modal
</button>

<svelte:window bind:innerHeight={windowHeight} bind:innerWidth={windowWidth} />

{#if windowHeight === 0 || windowWidth === 0}
	<p>Loading...</p>
{:else}
	<Table data={dataLoaded} />
{/if}

<dialog bind:this={modal} id="form-modal" class="modal z-50">
	<div class="modal-box">
		<Form
			onAccept={(results) => {
				dataLoaded = results;
			}}
		/>
		<div class="modal-action">
			<button class="btn" onclick={() => modal?.close()}>Close</button>
		</div>
	</div>
</dialog>

<style>
</style>
