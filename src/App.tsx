import React from 'react';
import { Dashboard } from './components/Dashboard';
import './App.css';

// Sample data based on our Python engine demo
const sampleGameState = {
  stage: '3',
  round_num: 2,
  level: 5,
  gold: 32,
  health: 78,
  board: {
    champions: [
      { name: 'Caitlyn', cost: 2, count: 2 },
      { name: 'Vi', cost: 3, count: 1 },
      { name: 'Darius', cost: 1, count: 2 },
      { name: 'Warwick', cost: 2, count: 1 },
    ],
    active_traits: {
      Sniper: 1,
      Enforcer: 2,
      Bruiser: 2,
    },
  },
};

const sampleBuildRecommendations = [
  {
    name: 'Sniper Reroll',
    tier: 'S',
    viability_score: 70.8,
    probability: 70.8,
    owned_champions: 2,
    contest_count: 0,
    reasoning: [
      'S-tier composition (WR: 54.0%)',
      'You own 2/7 champions (29%)',
      '✓ Uncontested',
      '✓ Perfect timing for this comp',
    ],
    next_steps: [
      'Find core units: Jinx',
      'Find carry: Jinx',
      'Level to 7+ for better odds',
      'Build items on Caitlyn: Giant Slayer, Last Whisper',
    ],
    champions: ['Caitlyn', 'Jinx', 'Miss Fortune', 'Urgot', 'Vi', 'Jayce', 'Ekko'],
    traits: ['Sniper', 'Enforcer', 'Rebel'],
    items: {
      Caitlyn: ['Giant Slayer', 'Last Whisper', "Runaan's Hurricane"],
      Jinx: ['Giant Slayer', "Runaan's Hurricane", 'Infinity Edge'],
    },
  },
  {
    name: 'Bruiser Frontline',
    tier: 'A',
    viability_score: 52.8,
    probability: 52.8,
    owned_champions: 3,
    contest_count: 1,
    reasoning: [
      'A-tier composition (WR: 52.0%)',
      'You own 3/6 champions (50%)',
      '⚠️ 1 opponent contesting',
      '✓ Perfect timing for this comp',
    ],
    next_steps: [
      'Find core units: Sett, Urgot',
      'Find carry: Sett',
      'Level to 7+ for better odds',
      "Build items on Sett: Sunfire Cape, Warmog's Armor",
    ],
    champions: ['Sett', 'Vi', 'Urgot', 'Warwick', 'Darius', 'Illaoi'],
    traits: ['Bruiser', 'Enforcer'],
    items: {
      Sett: ["Sunfire Cape", "Warmog's Armor", "Titan's Resolve"],
    },
  },
  {
    name: 'Fast 8 Legendaries',
    tier: 'B',
    viability_score: 46.6,
    probability: 46.6,
    owned_champions: 0,
    contest_count: 0,
    reasoning: [
      'B-tier composition (WR: 48.0%)',
      'You own 0/4 champions (0%)',
      '✓ Uncontested',
    ],
    next_steps: [
      'Find core units: Miss Fortune, Urgot',
      'Find carry: Miss Fortune',
      'Level to 7+ for better odds',
      'Build items on Miss Fortune: Giant Slayer, Last Whisper',
    ],
    champions: ['Miss Fortune', 'Urgot', 'Ekko', 'Viktor'],
    traits: ['Sniper', 'Mercenary'],
    items: {
      'Miss Fortune': ['Giant Slayer', 'Last Whisper', 'Infinity Edge'],
    },
  },
];

const sampleShopRecommendations = [
  {
    name: 'Caitlyn',
    type: 'champion' as const,
    priority: 'CRITICAL' as const,
    score: 100,
    reasoning: ['⭐⭐ 2-star upgrade available!'],
    metadata: {
      cost: 2,
      builds: ['Sniper Reroll'],
    },
  },
  {
    name: 'Jinx',
    type: 'champion' as const,
    priority: 'HIGH' as const,
    score: 75,
    reasoning: ['Main carry unit for comp', 'Used in: Sniper Reroll'],
    metadata: {
      cost: 3,
      is_carry: true,
      builds: ['Sniper Reroll'],
    },
  },
  {
    name: 'Jayce',
    type: 'champion' as const,
    priority: 'LOW' as const,
    score: 30,
    reasoning: ['Filler unit for comp', 'Used in: Sniper Reroll'],
    metadata: {
      cost: 3,
      builds: ['Sniper Reroll'],
    },
  },
  {
    name: 'Ezreal',
    type: 'champion' as const,
    priority: 'LOW' as const,
    score: 10,
    reasoning: ['Not in target builds'],
    metadata: {
      cost: 1,
    },
  },
  {
    name: 'Blitzcrank',
    type: 'champion' as const,
    priority: 'LOW' as const,
    score: 10,
    reasoning: ['Not in target builds'],
    metadata: {
      cost: 2,
    },
  },
];

const sampleAugmentRecommendations = [
  {
    name: 'Sniper Emblem',
    type: 'augment' as const,
    priority: 'MEDIUM' as const,
    score: 62.0,
    reasoning: ['A-tier augment'],
    metadata: {
      tier: 'A',
      breakdown: {
        tier: 0.32,
        board_synergy: 0.3,
        build_synergy: 0.0,
      },
    },
  },
  {
    name: 'Rich Get Richer',
    type: 'augment' as const,
    priority: 'LOW' as const,
    score: 40.0,
    reasoning: ['S-tier augment'],
    metadata: {
      tier: 'S',
      breakdown: {
        tier: 0.4,
        board_synergy: 0.0,
        build_synergy: 0.0,
      },
    },
  },
  {
    name: 'Combat Training',
    type: 'augment' as const,
    priority: 'LOW' as const,
    score: 24.0,
    reasoning: ['B-tier augment'],
    metadata: {
      tier: 'B',
      breakdown: {
        tier: 0.24,
        board_synergy: 0.0,
        build_synergy: 0.0,
      },
    },
  },
];

const sampleActionRecommendation = {
  action: 'roll',
  reasoning: 'Weak board - roll to improve',
  board_strength: 22.0,
};

function App() {
  return (
    <Dashboard
      gameState={sampleGameState}
      buildRecommendations={sampleBuildRecommendations}
      shopRecommendations={sampleShopRecommendations}
      augmentRecommendations={sampleAugmentRecommendations}
      actionRecommendation={sampleActionRecommendation}
    />
  );
}

export default App;
