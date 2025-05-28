export type PackageJson = {
	name?: string;
	version?: string;
	description?: string;
	main?: string;
	scripts?: Record<string, string>;
	dependencies?: Record<string, string>;
	devDependencies?: Record<string, string>;
	peerDependencies?: Record<string, string>;
	[key: string]: unknown;
};

export type PackageResult = {
	repo_path: string;
	package?: PackageJson;
	error?: string;
};

export type GraphNode = {
	id: string;
  type: 'node';
  value: number;
  name: string;
  children: Graph[];
};

export type GraphLeaf = {
	id: string;
  type: 'leaf';
  name: string;
  value: number;
};

export type Graph = GraphNode | GraphLeaf;