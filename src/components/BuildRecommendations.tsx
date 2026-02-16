import React from 'react';

interface Champion {
  name: string;
  cost: number;
}

interface BuildRecommendation {
  name: string;
  tier: string;
  viability_score: number;
  probability: number;
  owned_champions: number;
  contest_count: number;
  reasoning: string[];
  next_steps: string[];
  champions: string[];
  traits: string[];
  items: Record<string, string[]>;
}

interface Props {
  recommendations: BuildRecommendation[];
  onSelectBuild?: (build: BuildRecommendation) => void;
}

export const BuildRecommendations: React.FC<Props> = ({ recommendations, onSelectBuild }) => {
  const getTierColor = (tier: string) => {
    const colors: Record<string, string> = {
      S: 'text-red-500 bg-red-100',
      A: 'text-orange-500 bg-orange-100',
      B: 'text-yellow-500 bg-yellow-100',
      C: 'text-blue-500 bg-blue-100',
      D: 'text-gray-500 bg-gray-100',
    };
    return colors[tier] || colors['C'];
  };

  const getViabilityColor = (score: number) => {
    if (score >= 70) return 'text-green-600 bg-green-100';
    if (score >= 50) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getContestIcon = (count: number) => {
    if (count === 0) return '✓';
    if (count === 1) return '⚠️';
    return '🚫';
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-gray-800">🎯 Build Recommendations</h2>
        <span className="text-sm text-gray-500">Top {recommendations.length} Builds</span>
      </div>

      {recommendations.map((build, index) => (
        <div
          key={build.name}
          className="border border-gray-200 rounded-lg p-5 hover:shadow-lg transition-shadow cursor-pointer bg-white"
          onClick={() => onSelectBuild?.(build)}
        >
          {/* Header */}
          <div className="flex items-start justify-between mb-3">
            <div className="flex items-center gap-3">
              <span className="text-2xl font-bold text-gray-400">#{index + 1}</span>
              <div>
                <h3 className="text-xl font-bold text-gray-800">{build.name}</h3>
                <div className="flex items-center gap-2 mt-1">
                  <span className={`px-2 py-1 rounded-md text-xs font-bold ${getTierColor(build.tier)}`}>
                    {build.tier} TIER
                  </span>
                  <span className="text-xs text-gray-500">
                    {build.champions.length} champions
                  </span>
                </div>
              </div>
            </div>

            {/* Viability Score */}
            <div className="text-right">
              <div className={`text-3xl font-bold ${getViabilityColor(build.viability_score)}`}>
                {build.viability_score.toFixed(0)}
              </div>
              <div className="text-xs text-gray-500 uppercase">Viability</div>
            </div>
          </div>

          {/* Stats Row */}
          <div className="grid grid-cols-3 gap-4 mb-4 p-3 bg-gray-50 rounded-md">
            <div className="text-center">
              <div className="text-lg font-bold text-gray-700">{build.probability.toFixed(0)}%</div>
              <div className="text-xs text-gray-500">Success Rate</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-bold text-gray-700">
                {build.owned_champions}/{build.champions.length}
              </div>
              <div className="text-xs text-gray-500">Owned</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-bold text-gray-700">
                {getContestIcon(build.contest_count)} {build.contest_count}
              </div>
              <div className="text-xs text-gray-500">Contested</div>
            </div>
          </div>

          {/* Traits */}
          <div className="mb-3">
            <div className="flex flex-wrap gap-2">
              {build.traits.map((trait) => (
                <span
                  key={trait}
                  className="px-2 py-1 bg-purple-100 text-purple-700 rounded-md text-xs font-medium"
                >
                  {trait}
                </span>
              ))}
            </div>
          </div>

          {/* Reasoning */}
          <div className="mb-3">
            <h4 className="text-sm font-semibold text-gray-700 mb-2">Why this build:</h4>
            <ul className="space-y-1">
              {build.reasoning.map((reason, i) => (
                <li key={i} className="text-sm text-gray-600 flex items-start">
                  <span className="mr-2">•</span>
                  <span>{reason}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Next Steps */}
          <div className="border-t border-gray-200 pt-3">
            <h4 className="text-sm font-semibold text-gray-700 mb-2">Next Steps:</h4>
            <ul className="space-y-1">
              {build.next_steps.map((step, i) => (
                <li key={i} className="text-sm text-blue-600 flex items-start">
                  <span className="mr-2">→</span>
                  <span className="font-medium">{step}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Expand button hint */}
          <div className="text-center mt-3 pt-3 border-t border-gray-100">
            <span className="text-xs text-gray-400">Click to see full details</span>
          </div>
        </div>
      ))}
    </div>
  );
};
