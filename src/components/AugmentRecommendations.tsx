import React from 'react';

interface AugmentRecommendation {
  name: string;
  type: 'augment';
  priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  score: number;
  reasoning: string[];
  metadata: {
    tier: string;
    breakdown?: Record<string, number>;
  };
}

interface Props {
  recommendations: AugmentRecommendation[];
  onSelectAugment?: (augment: AugmentRecommendation) => void;
}

export const AugmentRecommendations: React.FC<Props> = ({ recommendations, onSelectAugment }) => {
  const getTierColor = (tier: string) => {
    const colors: Record<string, { text: string; bg: string; border: string }> = {
      S: { text: 'text-red-600', bg: 'bg-red-100', border: 'border-red-300' },
      A: { text: 'text-orange-600', bg: 'bg-orange-100', border: 'border-orange-300' },
      B: { text: 'text-yellow-600', bg: 'bg-yellow-100', border: 'border-yellow-300' },
      C: { text: 'text-blue-600', bg: 'bg-blue-100', border: 'border-blue-300' },
      D: { text: 'text-gray-600', bg: 'bg-gray-100', border: 'border-gray-300' },
    };
    return colors[tier] || colors['C'];
  };

  const getScoreGradient = (score: number) => {
    if (score >= 80) return 'from-green-500 to-green-600';
    if (score >= 60) return 'from-yellow-500 to-yellow-600';
    if (score >= 40) return 'from-orange-500 to-orange-600';
    return 'from-red-500 to-red-600';
  };

  const getPriorityBadge = (priority: string) => {
    const configs: Record<string, { text: string; bg: string }> = {
      HIGH: { text: 'text-green-700', bg: 'bg-green-100' },
      MEDIUM: { text: 'text-yellow-700', bg: 'bg-yellow-100' },
      LOW: { text: 'text-gray-700', bg: 'bg-gray-100' },
    };
    return configs[priority] || configs['LOW'];
  };

  const getRecommendationIcon = (index: number) => {
    if (index === 0) return '⭐';
    if (index === 1) return '👍';
    return '👌';
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="mb-4">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">✨ Augment Recommendations</h2>
        <p className="text-sm text-gray-600">Choose wisely - augments are permanent!</p>
      </div>

      {/* Recommendations */}
      <div className="space-y-3">
        {recommendations.map((rec, index) => {
          const tierConfig = getTierColor(rec.metadata.tier);
          const priorityConfig = getPriorityBadge(rec.priority);
          const scoreGradient = getScoreGradient(rec.score);

          return (
            <div
              key={rec.name}
              className={`border-2 rounded-lg p-5 cursor-pointer hover:shadow-lg transition-all ${
                index === 0 ? 'border-green-400 bg-green-50' : 'border-gray-200 bg-white'
              }`}
              onClick={() => onSelectAugment?.(rec)}
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-2xl">{getRecommendationIcon(index)}</span>
                    <h3 className="text-xl font-bold text-gray-800">{rec.name}</h3>
                    {index === 0 && (
                      <span className="px-2 py-1 bg-green-200 text-green-800 rounded-md text-xs font-bold">
                        BEST CHOICE
                      </span>
                    )}
                  </div>

                  {/* Badges */}
                  <div className="flex items-center gap-2 flex-wrap">
                    <span
                      className={`px-2 py-1 rounded-md text-xs font-bold ${tierConfig.text} ${tierConfig.bg}`}
                    >
                      {rec.metadata.tier}-TIER
                    </span>
                    <span
                      className={`px-2 py-1 rounded-md text-xs font-bold ${priorityConfig.text} ${priorityConfig.bg}`}
                    >
                      {rec.priority}
                    </span>
                  </div>
                </div>

                {/* Score Display */}
                <div className="text-right ml-4">
                  <div className="relative">
                    <div
                      className={`text-3xl font-bold bg-gradient-to-r ${scoreGradient} text-transparent bg-clip-text`}
                    >
                      {rec.score.toFixed(0)}
                    </div>
                    <div className="text-xs text-gray-500 uppercase">Score</div>
                  </div>
                </div>
              </div>

              {/* Score Breakdown Bar */}
              <div className="mb-3">
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className={`h-full bg-gradient-to-r ${scoreGradient} transition-all duration-500`}
                    style={{ width: `${rec.score}%` }}
                  />
                </div>
              </div>

              {/* Reasoning */}
              <div className="space-y-1 mb-3">
                {rec.reasoning.map((reason, i) => (
                  <div key={i} className="flex items-start text-sm text-gray-700">
                    <span className="mr-2">✓</span>
                    <span>{reason}</span>
                  </div>
                ))}
              </div>

              {/* Breakdown if available */}
              {rec.metadata.breakdown && (
                <div className="pt-3 border-t border-gray-200">
                  <div className="text-xs text-gray-600 space-y-1">
                    <div className="font-semibold mb-1">Score Breakdown:</div>
                    {Object.entries(rec.metadata.breakdown).map(([key, value]) => (
                      <div key={key} className="flex justify-between">
                        <span className="capitalize">{key.replace('_', ' ')}:</span>
                        <span className="font-medium">{(value * 10).toFixed(1)}/10</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Best choice indicator */}
              {index === 0 && (
                <div className="mt-3 pt-3 border-t border-green-200">
                  <div className="text-sm text-green-700 font-medium text-center">
                    ⬆️ This augment has the best synergy with your strategy
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Empty state */}
      {recommendations.length === 0 && (
        <div className="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
          <div className="text-5xl mb-3">🎁</div>
          <div className="text-lg font-semibold text-gray-700 mb-1">No Augments Available</div>
          <div className="text-sm text-gray-500">Augments appear at specific stages</div>
        </div>
      )}
    </div>
  );
};
