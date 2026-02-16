import React from 'react';

interface ShopRecommendation {
  name: string;
  type: 'champion';
  priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'AVOID';
  score: number;
  reasoning: string[];
  metadata: {
    cost: number;
    is_carry?: boolean;
    is_core?: boolean;
    builds?: string[];
  };
}

interface Props {
  recommendations: ShopRecommendation[];
  currentGold: number;
}

export const ShopRecommendations: React.FC<Props> = ({ recommendations, currentGold }) => {
  const getPriorityConfig = (priority: string) => {
    const configs: Record<string, { emoji: string; color: string; bg: string; border: string }> = {
      CRITICAL: {
        emoji: '🔴',
        color: 'text-red-700',
        bg: 'bg-red-50',
        border: 'border-red-300',
      },
      HIGH: {
        emoji: '🟠',
        color: 'text-orange-700',
        bg: 'bg-orange-50',
        border: 'border-orange-300',
      },
      MEDIUM: {
        emoji: '🟡',
        color: 'text-yellow-700',
        bg: 'bg-yellow-50',
        border: 'border-yellow-300',
      },
      LOW: {
        emoji: '⚪',
        color: 'text-gray-700',
        bg: 'bg-gray-50',
        border: 'border-gray-300',
      },
      AVOID: {
        emoji: '⛔',
        color: 'text-gray-500',
        bg: 'bg-gray-100',
        border: 'border-gray-400',
      },
    };
    return configs[priority] || configs['LOW'];
  };

  const getCostColor = (cost: number) => {
    const colors: Record<number, string> = {
      1: 'text-gray-500',
      2: 'text-green-500',
      3: 'text-blue-500',
      4: 'text-purple-500',
      5: 'text-yellow-500',
    };
    return colors[cost] || 'text-gray-500';
  };

  const getCostBg = (cost: number) => {
    const colors: Record<number, string> = {
      1: 'bg-gray-200',
      2: 'bg-green-200',
      3: 'bg-blue-200',
      4: 'bg-purple-200',
      5: 'bg-yellow-200',
    };
    return colors[cost] || 'bg-gray-200';
  };

  const canAfford = (cost: number) => {
    return currentGold >= cost;
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-gray-800">🛒 Shop Recommendations</h2>
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-500">Gold:</span>
          <span className="text-xl font-bold text-yellow-600">{currentGold}</span>
        </div>
      </div>

      {/* Priority Legend */}
      <div className="flex gap-2 text-xs mb-4 p-3 bg-gray-50 rounded-md">
        <span className="font-semibold text-gray-700">Priority:</span>
        <span>🔴 Critical</span>
        <span>🟠 High</span>
        <span>🟡 Medium</span>
        <span>⚪ Low</span>
      </div>

      {/* Recommendations */}
      <div className="space-y-2">
        {recommendations.map((rec, index) => {
          const config = getPriorityConfig(rec.priority);
          const affordable = canAfford(rec.metadata.cost);

          return (
            <div
              key={`${rec.name}-${index}`}
              className={`border-2 rounded-lg p-4 ${config.bg} ${config.border} ${
                !affordable ? 'opacity-50' : ''
              }`}
            >
              {/* Champion Header */}
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{config.emoji}</span>
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className={`text-lg font-bold ${config.color}`}>{rec.name}</h3>
                      <span
                        className={`px-2 py-0.5 rounded text-xs font-bold ${getCostColor(
                          rec.metadata.cost
                        )} ${getCostBg(rec.metadata.cost)}`}
                      >
                        {rec.metadata.cost}g
                      </span>
                    </div>
                    <div className="flex items-center gap-2 mt-1">
                      <span className={`text-xs font-bold ${config.color}`}>{rec.priority}</span>
                      {rec.metadata.is_carry && (
                        <span className="px-2 py-0.5 bg-red-200 text-red-700 rounded text-xs font-bold">
                          CARRY
                        </span>
                      )}
                      {rec.metadata.is_core && (
                        <span className="px-2 py-0.5 bg-blue-200 text-blue-700 rounded text-xs font-bold">
                          CORE
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Score */}
                <div className="text-right">
                  <div className={`text-2xl font-bold ${config.color}`}>{rec.score.toFixed(0)}</div>
                  <div className="text-xs text-gray-500">Score</div>
                </div>
              </div>

              {/* Reasoning */}
              <ul className="space-y-1 mb-2">
                {rec.reasoning.map((reason, i) => (
                  <li key={i} className="text-sm text-gray-700 flex items-start">
                    <span className="mr-2">•</span>
                    <span>{reason}</span>
                  </li>
                ))}
              </ul>

              {/* Builds this is used in */}
              {rec.metadata.builds && rec.metadata.builds.length > 0 && (
                <div className="mt-2 pt-2 border-t border-gray-200">
                  <div className="flex flex-wrap gap-1">
                    {rec.metadata.builds.map((build) => (
                      <span
                        key={build}
                        className="px-2 py-0.5 bg-purple-100 text-purple-700 rounded text-xs"
                      >
                        {build}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Afford warning */}
              {!affordable && (
                <div className="mt-2 pt-2 border-t border-gray-200">
                  <span className="text-xs text-red-600 font-medium">
                    ⚠️ Not enough gold ({rec.metadata.cost}g needed)
                  </span>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Empty state */}
      {recommendations.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          <div className="text-4xl mb-2">🔄</div>
          <div>Reroll to see recommendations</div>
        </div>
      )}
    </div>
  );
};
