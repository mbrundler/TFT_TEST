import React, { useState } from 'react';
import { GameStateDisplay } from './GameStateDisplay';
import { BuildRecommendations } from './BuildRecommendations';
import { ShopRecommendations } from './ShopRecommendations';
import { AugmentRecommendations } from './AugmentRecommendations';

interface DashboardProps {
  gameState: any;
  buildRecommendations: any[];
  shopRecommendations: any[];
  augmentRecommendations: any[];
  actionRecommendation: any;
}

export const Dashboard: React.FC<DashboardProps> = ({
  gameState,
  buildRecommendations,
  shopRecommendations,
  augmentRecommendations,
  actionRecommendation,
}) => {
  const [selectedTab, setSelectedTab] = useState<'builds' | 'shop' | 'augments'>('builds');

  const tabs = [
    { id: 'builds' as const, label: '🎯 Builds', count: buildRecommendations.length },
    { id: 'shop' as const, label: '🛒 Shop', count: shopRecommendations.length },
    { id: 'augments' as const, label: '✨ Augments', count: augmentRecommendations.length },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-800">TFT Meta Guide</h1>
              <p className="text-sm text-gray-600 mt-1">
                AI-powered recommendations for Teamfight Tactics
              </p>
            </div>
            <div className="flex items-center gap-3">
              <div className="text-right">
                <div className="text-xs text-gray-500">Patch</div>
                <div className="text-sm font-semibold text-gray-700">14.2</div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Game State */}
          <div className="lg:col-span-1">
            <GameStateDisplay gameState={gameState} actionRecommendation={actionRecommendation} />
          </div>

          {/* Right Column - Recommendations */}
          <div className="lg:col-span-2">
            {/* Tabs */}
            <div className="bg-white border border-gray-200 rounded-lg shadow-sm mb-4">
              <div className="flex border-b border-gray-200">
                {tabs.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setSelectedTab(tab.id)}
                    className={`flex-1 px-6 py-4 text-center font-medium transition-colors relative ${
                      selectedTab === tab.id
                        ? 'text-blue-600 bg-blue-50'
                        : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center justify-center gap-2">
                      <span>{tab.label}</span>
                      {tab.count > 0 && (
                        <span
                          className={`px-2 py-0.5 rounded-full text-xs font-bold ${
                            selectedTab === tab.id
                              ? 'bg-blue-200 text-blue-700'
                              : 'bg-gray-200 text-gray-600'
                          }`}
                        >
                          {tab.count}
                        </span>
                      )}
                    </div>
                    {selectedTab === tab.id && (
                      <div className="absolute bottom-0 left-0 right-0 h-1 bg-blue-600" />
                    )}
                  </button>
                ))}
              </div>

              {/* Tab Content */}
              <div className="p-6">
                {selectedTab === 'builds' && (
                  <BuildRecommendations
                    recommendations={buildRecommendations}
                    onSelectBuild={(build) => console.log('Selected build:', build)}
                  />
                )}

                {selectedTab === 'shop' && (
                  <ShopRecommendations
                    recommendations={shopRecommendations}
                    currentGold={gameState.gold}
                  />
                )}

                {selectedTab === 'augments' && (
                  <AugmentRecommendations
                    recommendations={augmentRecommendations}
                    onSelectAugment={(aug) => console.log('Selected augment:', aug)}
                  />
                )}
              </div>
            </div>

            {/* Help Section */}
            <div className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
              <h3 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                <span>💡</span>
                <span>How to Use</span>
              </h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• <strong>Builds:</strong> Shows top meta comps based on your current board</li>
                <li>• <strong>Shop:</strong> Prioritizes which champions to buy from your shop</li>
                <li>• <strong>Augments:</strong> Scores augment choices based on synergy</li>
                <li>• Priority levels: 🔴 Critical → 🟠 High → 🟡 Medium → ⚪ Low</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="text-center text-sm text-gray-500">
            <p>Built with ❤️ for TFT players</p>
            <p className="mt-1">
              Data sources: tactics.tools • MetaTFT • Community Dragon
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};
