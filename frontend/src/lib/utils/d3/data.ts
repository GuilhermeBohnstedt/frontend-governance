import type { Graph } from '$lib/models';

export const data: Graph = {
  id: 'boss',
  type: 'node',
  name: 'boss',
  value: 0,
  children: [
    {
      id: 'team-dataviz',
      type: 'node',
      name: 'Team Dataviz',
      value: 0,
      children: [
        { id: 'mark', type: 'leaf', name: 'Mark', value: 90 },
        { id: 'robert', type: 'leaf', name: 'Robert', value: 12 },
        { id: 'emily', type: 'leaf', name: 'Emily', value: 34 },
        { id: 'marion', type: 'leaf', name: 'Marion', value: 53 }
      ]
    },
    {
      id: 'team-devops',
      type: 'node',
      name: 'Team DevOps',
      value: 0,
      children: [
        { id: 'nicolas', type: 'leaf', name: 'Nicolas', value: 98 },
        { id: 'malki', type: 'leaf', name: 'Malki', value: 22 },
        { id: 'dje', type: 'leaf', name: 'Djé', value: 12 }
      ]
    },
    {
      id: 'team-sales',
      type: 'node',
      name: 'Team Sales',
      value: 0,
      children: [
        { id: 'melanie', type: 'leaf', name: 'Mélanie', value: 45 },
        { id: 'einstein', type: 'leaf', name: 'Einstein', value: 76 }
      ]
    }
  ]
};
