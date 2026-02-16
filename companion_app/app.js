// TFT Meta Guide - Companion App JavaScript

const API_URL = 'http://localhost:5000';

// Current game state
let currentRecommendations = null;

// Quick action buttons
function quickLevel() {
    const levelInput = document.getElementById('level');
    levelInput.value = Math.min(10, parseInt(levelInput.value) + 1);

    // Deduct gold (costs based on level)
    const goldInput = document.getElementById('gold');
    const level = parseInt(levelInput.value);
    const cost = [0, 0, 2, 6, 10, 20, 36, 56, 80][level - 1] || 0;
    goldInput.value = Math.max(0, parseInt(goldInput.value) - cost);
}

function quickRoll() {
    const goldInput = document.getElementById('gold');
    goldInput.value = Math.max(0, parseInt(goldInput.value) - 2);
}

function quickBuy() {
    const goldInput = document.getElementById('gold');
    const levelInput = document.getElementById('level');
    const cost = Math.min(5, parseInt(levelInput.value)); // Champions cost 1-5 based on tier
    goldInput.value = Math.max(0, parseInt(goldInput.value) - cost);
}

function quickSell() {
    const goldInput = document.getElementById('gold');
    goldInput.value = parseInt(goldInput.value) + 1; // Selling gives 1 gold
}

// Switch tabs
function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    event.target.classList.add('active');

    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tabName}-content`).classList.add('active');
}

// Get recommendations from API
async function getRecommendations() {
    const actionContent = document.getElementById('action-content');
    const buildsContent = document.getElementById('builds-content');
    const shopContent = document.getElementById('shop-content');
    const augmentsContent = document.getElementById('augments-content');

    // Show loading
    actionContent.innerHTML = '<div class="loading">⏳ Analyzing game state...</div>';
    buildsContent.innerHTML = '<div class="loading">⏳ Loading...</div>';
    shopContent.innerHTML = '<div class="loading">⏳ Loading...</div>';
    augmentsContent.innerHTML = '<div class="loading">⏳ Loading...</div>';

    try {
        // Build payload
        const payload = buildPayload();

        // Call API
        const response = await fetch(`${API_URL}/api/recommend-all`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        currentRecommendations = data;

        // Render results
        renderAction(data.action);
        renderBuilds(data.builds);
        renderShop(data.shop);
        renderAugments(data.augments);

    } catch (error) {
        console.error('Error:', error);
        const errorHtml = `
            <div class="error">
                ❌ Error: ${error.message}<br>
                Make sure the API server is running: <code>python backend/api.py</code>
            </div>
        `;
        actionContent.innerHTML = errorHtml;
        buildsContent.innerHTML = errorHtml;
        shopContent.innerHTML = errorHtml;
        augmentsContent.innerHTML = errorHtml;
    }
}

// Build API payload from inputs
function buildPayload() {
    const stage = document.getElementById('stage').value;
    const level = parseInt(document.getElementById('level').value);
    const gold = parseInt(document.getElementById('gold').value);
    const health = parseInt(document.getElementById('health').value);

    // Parse board champions
    const boardChampionsInput = document.getElementById('board-champions').value;
    const boardChampions = boardChampionsInput
        .split(',')
        .map(name => name.trim())
        .filter(name => name.length > 0)
        .map(name => ({
            name: name,
            cost: 1, // Can be enhanced
            level: 1,
            items: []
        }));

    // Parse shop
    const shopInput = document.getElementById('shop').value;
    const shop = shopInput
        .split(',')
        .map(name => name.trim())
        .filter(name => name.length > 0);

    // Parse augments
    const augmentsInput = document.getElementById('augments').value;
    const augments = augmentsInput
        .split(',')
        .map(name => name.trim())
        .filter(name => name.length > 0);

    return {
        stage,
        level,
        gold,
        health,
        board: {
            champions: boardChampions,
            traits: [] // Can be enhanced
        },
        bench: [],
        item_components: [],
        completed_items: [],
        shop: shop.length > 0 ? shop : undefined,
        augment_choices: augments.length > 0 ? augments : undefined
    };
}

// Render action recommendation
function renderAction(action) {
    const container = document.getElementById('action-content');

    const html = `
        <div class="action-card">
            <h3>${action.recommendation}</h3>
            <p class="action-reason">${action.reason}</p>
            <p style="margin-top: 10px; font-size: 18px;">
                Board Strength: <strong>${action.board_strength}/100</strong>
            </p>
        </div>
        <div class="rec-details" style="text-align: center; margin-top: 20px;">
            <p><strong>What to do next:</strong></p>
            <p style="margin-top: 10px;">
                ${action.recommendation === 'ROLL' ?
                    '🎲 Roll down to find your key champions and upgrades' :
                    '💰 Save gold to gain interest (max 5g per round)'
                }
            </p>
        </div>
    `;

    container.innerHTML = html;
}

// Render build recommendations
function renderBuilds(builds) {
    const container = document.getElementById('builds-content');

    if (!builds || builds.length === 0) {
        container.innerHTML = '<div class="loading">No build recommendations available</div>';
        return;
    }

    const html = builds.map((build, index) => {
        const viabilityClass = build.viability >= 70 ? 'high' :
                               build.viability >= 50 ? 'medium' : 'low';

        const tier = build.viability >= 70 ? 'S' :
                     build.viability >= 60 ? 'A' :
                     build.viability >= 50 ? 'B' : 'C';

        return `
            <div class="rec-card">
                <div class="rec-header">
                    <div>
                        <span style="color: #aaa; font-size: 14px;">#${index + 1}</span>
                        <span class="rec-title"> ${build.name}</span>
                    </div>
                    <div style="display: flex; gap: 10px; align-items: center;">
                        <span style="background: rgba(255,215,0,0.2); padding: 4px 10px; border-radius: 12px; font-size: 12px;">${tier}</span>
                        <span class="viability ${viabilityClass}">${build.viability.toFixed(1)}/100</span>
                    </div>
                </div>

                <div class="traits">
                    ${build.traits.map(trait => `<span class="trait-badge">${trait}</span>`).join('')}
                </div>

                <div class="rec-details">
                    <p><strong>Core Champions:</strong> ${build.champions.map(c => c.name).join(', ')}</p>
                    <p style="margin-top: 8px;"><strong>Why:</strong> ${build.reason}</p>
                    ${build.contested ? `<p style="color: #ff8c00; margin-top: 5px;">⚠️ Contested by ${build.num_opponents} opponent(s)</p>` : ''}
                </div>

                <div class="next-steps">
                    <strong>📋 Next Steps:</strong><br>
                    ${build.next_steps.map(step => `• ${step}`).join('<br>')}
                </div>
            </div>
        `;
    }).join('');

    container.innerHTML = html;
}

// Render shop recommendations
function renderShop(shop) {
    const container = document.getElementById('shop-content');

    if (!shop || shop.length === 0) {
        container.innerHTML = '<div class="loading">Enter shop champions to get recommendations</div>';
        return;
    }

    const html = shop.map(item => {
        const priorityClass = item.priority.toLowerCase();
        const priorityIcon = {
            'CRITICAL': '🔴',
            'HIGH': '🟠',
            'MEDIUM': '🟡',
            'LOW': '⚪'
        }[item.priority] || '⚪';

        return `
            <div class="shop-item ${priorityClass}">
                <div>
                    <div class="shop-name">
                        ${priorityIcon} ${item.champion}
                        ${item.is_upgrade ? ' ⭐⭐' : ''}
                    </div>
                    <div class="shop-reason">${item.reason}</div>
                    ${!item.can_afford ? '<div class="shop-reason" style="color: #ff4444;">❌ Cannot afford</div>' : ''}
                </div>
                <div class="shop-score">${item.score.toFixed(0)}</div>
            </div>
        `;
    }).join('');

    container.innerHTML = html;
}

// Render augment recommendations
function renderAugments(augments) {
    const container = document.getElementById('augments-content');

    if (!augments || augments.length === 0) {
        container.innerHTML = '<div class="loading">Enter augment choices to get recommendations</div>';
        return;
    }

    const html = augments.map((aug, index) => {
        const tierColor = {
            'S': '#ffd700',
            'A': '#00ff88',
            'B': '#4facfe',
            'C': '#aaa',
            'D': '#888'
        }[aug.tier] || '#888';

        return `
            <div class="rec-card" style="border-left: 4px solid ${tierColor};">
                <div class="rec-header">
                    <div class="rec-title">${aug.name}</div>
                    <div style="display: flex; gap: 10px; align-items: center;">
                        <span style="background: ${tierColor}; color: #000; padding: 4px 10px; border-radius: 12px; font-weight: bold;">${aug.tier}</span>
                        <span class="viability high">${aug.score.toFixed(0)}/100</span>
                    </div>
                </div>

                <div class="rec-details">
                    <p><strong>Why:</strong> ${aug.reason}</p>
                    ${aug.synergies.length > 0 ? `
                        <p style="margin-top: 8px;"><strong>Synergies:</strong> ${aug.synergies.join(', ')}</p>
                    ` : ''}
                </div>
            </div>
        `;
    }).join('');

    container.innerHTML = html;
}

// Test connection on load
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_URL}/api/health`);
        if (response.ok) {
            console.log('✅ Connected to API server');
        }
    } catch (error) {
        console.warn('⚠️ API server not running. Start it with: python backend/api.py');
    }
});
