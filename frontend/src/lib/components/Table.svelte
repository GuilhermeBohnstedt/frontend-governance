<script lang="ts">
	import type { PackageJson, PackageResult } from "$lib/models";

	interface Props {
		data: PackageResult[];
	}

	const { data }: Props = $props();
</script>

<div class="overflow-x-auto">
  <table class="table table-xs">
    <thead>
      <tr>
        <th>#</th>
        <th>Name</th>
        <th>Dependencies</th>
        <th>Dev Dependencies</th>
      </tr>
    </thead>
    <tbody>
      {#each data as pkg, i}
        <tr>
          <th>{i + 1}</th>
          <td>{pkg.package?.name}</td>
          <td>
            {#if pkg.package?.dependencies}
              <ul>
                {#each Object.entries(pkg.package.dependencies) as [dep, version]}
                  <li>{dep}: {version}</li>
                {/each}
              </ul>
            {:else}
                <span>-</span>
              {/if}
          </td>
          <td>
            {#if pkg.package?.devDependencies}
              <ul>
                {#each Object.entries(pkg.package.devDependencies) as [dep, version]}
                  <li>{dep}: {version}</li>
                {/each}
              </ul>
            {:else}
              <span>-</span>
            {/if}
          </td>
        </tr>
      {/each}
    </tbody>
    <tfoot>
      <tr>
        <th>#</th>
        <th>Name</th>
        <th>Dependencies</th>
        <th>Dev Dependencies</th>
      </tr>
    </tfoot>
  </table>
</div>