import React from 'react';

interface GameState {
  stage: string;
  round_num: number;
  level: number;
  gold: number;
  health: number;
  board: {
    champions: Array<{ name: string; cost: number; count: number }>;
    active_traits: Record<string, number>;
  };
}

interface ActionRecommendation {
  action: string;
  reasoning: string;
  board_strength: number;
}

interface Props {
  gameState: GameState;
  actionRecommendation?: ActionRecommendation;
}

export const GameStateDisplay: React.FC<Props> = ({ gameState, actionRecommendation }) => {
  const getHealthColor = (health: number) => {
    if (health >= 70) return 'text-green-600';
    if (health >= 40) return 'text-yellow-600';
    if (health >= 20) return 'text-orange-600';
    return 'text-red-600';
  };

  const getHealthBarColor = (health: number) => {
    if (health >= 70) return 'bg-green-500';
    if (health >= 40) return 'bg-yellow-500';
    if (health >= 20) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const getStrengthColor = (strength: number) => {
    if (strength >= 70) return 'text-green-600';
    if (strength >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getActionColor = (action: string) => {
    if (action.toLowerCase() === 'roll') return 'bg-red-100 text-red-700 border-red-300';
    if (action.toLowerCase() === 'eco') return 'bg-green-100 text-green-700 border-green-300';
    return 'bg-blue-100 text-blue-700 border-blue-300';
  };

  const getCostColor = (cost: number) => {
    const colors: Record<number, string> = {
      1: 'text-gray-600',
      2: 'text-green-600',
      3: 'text-blue-600',
      4: 'text-purple-600',
      5: 'text-yellow-600',
    };
    return colors[cost] || 'text-gray-600';
  };

  const getTraitTierColor = (tier: number) => {
    const colors: Record<number, string> = {
      1: 'bg-gray-200 text-gray-700',
      2: 'bg-green-200 text-green-700',
      3: 'bg-blue-200 text-blue-700',
      4: 'bg-purple-200 text-purple-700',
      5: 'bg-yellow-200 text-yellow-700',
    };
    return colors[tier] || 'bg-gray-200 text-gray-700';
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-800">📊 Game State</h2>
        <div className="text-sm text-gray-500">
          Stage {gameState.stage}-{gameState.round_num}
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Health */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="text-xs text-gray-500 uppercase mb-1">Health</div>
          <div className={`text-2xl font-bold ${getHealthColor(gameState.health)}`}>
            {gameState.health}
          </div>
          <div className="mt-2 h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className={`h-full ${getHealthBarColor(gameState.health)} transition-all`}
              style={{ width: `${gameState.health}%` }}
            />
          </div>
        </div>

        {/* Gold */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="text-xs text-gray-500 uppercase mb-1">Gold</div>
          <div className="text-2xl font-bold text-yellow-600">{gameState.gold}</div>
          <div className="text-xs text-gray-500 mt-1">
            {Math.floor(gameState.gold / 10)} interest
          </div>
        </div>

        {/* Level */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="text-xs text-gray-500 uppercase mb-1">Level</div>
          <div className="text-2xl font-bold text-blue-600">{gameState.level}</div>
          <div className="text-xs text-gray-500 mt-1">{gameState.board.champions.length} units</div>
        </div>

        {/* Stage */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="text-xs text-gray-500 uppercase mb-1">Stage</div>
          <div className="text-2xl font-bold text-purple-600">
            {gameState.stage}-{gameState.round_num}
          </div>
          <div className="text-xs text-gray-500 mt-1">
            {parseInt(gameState.stage) <= 3 ? 'Early' : parseInt(gameState.stage) <= 5 ? 'Mid' : 'Late'} Game
          </div>
        </div>
      </div>

      {/* Current Board */}
      <div className="bg-white border border-gray-200 rounded-lg p-4">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">Current Board</h3>
        <div className="space-y-2">
          {gameState.board.champions.map((champ, index) => (
            <div key={`${champ.name}-${index}`} className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className={`font-medium ${getCostColor(champ.cost)}`}>{champ.name}</span>
                <span className="text-xs text-gray-500">
                  {'⭐'.repeat(champ.count >= 3 ? 2 : 1)}
                </span>
              </div>
              <span className="text-xs text-gray-500">{champ.cost}g</span>
            </div>
          ))}
          {gameState.board.champions.length === 0 && (
            <div className="text-sm text-gray-500 text-center py-2">No champions on board</div>
          )}
        </div>
      </div>

      {/* Active Traits */}
      <div className="bg-white border border-gray-200 rounded-lg p-4">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">Active Traits</h3>
        <div className="flex flex-wrap gap-2">
          {Object.entries(gameState.board.active_traits).map(([trait, tier]) => (
            <span
              key={trait}
              className={`px-3 py-1 rounded-md text-sm font-medium ${getTraitTierColor(tier)}`}
            >
              {trait} ({tier})
            </span>
          ))}
          {Object.keys(gameState.board.active_traits).length === 0 && (
            <span className="text-sm text-gray-500">No active traits</span>
          )}
        </div>
      </div>

      {/* Action Recommendation */}
      {actionRecommendation && (
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-200 rounded-lg p-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
            <span>💡</span>
            <span>Recommended Action</span>
          </h3>

          <div className="space-y-3">
            {/* Action */}
            <div
              className={`inline-block px-4 py-2 rounded-lg text-lg font-bold border-2 ${getActionColor(
                actionRecommendation.action
              )}`}
            >
              {actionRecommendation.action.toUpperCase()}
            </div>

            {/* Reasoning */}
            <div className="text-sm text-gray-700">
              <span className="font-medium">Why: </span>
              {actionRecommendation.reasoning}
            </div>

            {/* Board Strength */}
            <div className="flex items-center gap-3">
              <span className="text-sm text-gray-600">Board Strength:</span>
              <div className="flex-1">
                <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className={`h-full transition-all ${
                      actionRecommendation.board_strength >= 70
                        ? 'bg-green-500'
                        : actionRecommendation.board_strength >= 50
                        ? 'bg-yellow-500'
                        : 'bg-red-500'
                    }`}
                    style={{ width: `${actionRecommendation.board_strength}%` }}
                  />
                </div>
              </div>
              <span
                className={`text-sm font-bold ${getStrengthColor(actionRecommendation.board_strength)}`}
              >
                {actionRecommendation.board_strength.toFixed(0)}/100
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
