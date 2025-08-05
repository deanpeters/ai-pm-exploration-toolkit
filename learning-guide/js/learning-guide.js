/**
 * AI PM Learning Guide - Interactive Learning Platform
 * Progressive Web App for Product Manager AI Skills Development
 */

class LearningGuide {
    constructor() {
        this.progress = this.loadProgress();
        this.currentTrack = null;
        this.searchIndex = null;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateProgress();
        this.loadRecentActivity();
        this.buildSearchIndex();
    }

    setupEventListeners() {
        // Track card clicks
        document.querySelectorAll('.track-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const track = e.currentTarget.dataset.track;
                this.startTrack(track);
            });
        });

        // Quick access buttons
        document.querySelectorAll('.quick-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const type = e.target.closest('.quick-card').dataset.type;
                const value = e.target.dataset[type];
                this.handleQuickAccess(type, value);
            });
        });

        // Search functionality
        const searchBtn = document.querySelector('.search-btn');
        const searchModal = document.querySelector('.search-modal');
        const searchClose = document.querySelector('.search-close');
        const searchInput = document.querySelector('.search-input');

        searchBtn.addEventListener('click', () => {
            searchModal.classList.remove('hidden');
            searchInput.focus();
        });

        searchClose.addEventListener('click', () => {
            searchModal.classList.add('hidden');
        });

        searchModal.addEventListener('click', (e) => {
            if (e.target === searchModal) {
                searchModal.classList.add('hidden');
            }
        });

        searchInput.addEventListener('input', (e) => {
            this.handleSearch(e.target.value);
        });

        // Progress button
        document.querySelector('.progress-btn').addEventListener('click', () => {
            this.showProgressModal();
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                searchModal.classList.add('hidden');
            }
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                searchModal.classList.remove('hidden');
                searchInput.focus();
            }
        });
    }

    startTrack(trackName) {
        // Store current track
        this.currentTrack = trackName;
        
        // Navigate to track page
        window.location.href = `tracks/${trackName}.html`;
        
        // Update progress
        if (!this.progress.tracks[trackName]) {
            this.progress.tracks[trackName] = {
                started: new Date().toISOString(),
                modules: {},
                progress: 0
            };
            this.saveProgress();
        }
    }

    handleQuickAccess(type, value) {
        const params = new URLSearchParams();
        params.set(type, value);
        
        // Navigate to filtered view
        window.location.href = `browse.html?${params.toString()}`;
    }

    handleSearch(query) {
        if (!query.trim()) {
            document.querySelector('.search-results').innerHTML = '';
            return;
        }

        const results = this.searchContent(query);
        this.displaySearchResults(results);
    }

    searchContent(query) {
        // Simple search implementation
        const searchTerms = query.toLowerCase().split(' ');
        
        const content = [
            // Tracks
            { type: 'track', id: 'collaboration', title: 'AI Collaboration', description: 'Better product briefs with AI writing', url: 'tracks/collaboration.html' },
            { type: 'track', id: 'research', title: 'Research & Analysis', description: 'Competitive intelligence and market research', url: 'tracks/research.html' },
            { type: 'track', id: 'visual', title: 'Visual Building', description: 'Demo without engineering using workflows', url: 'tracks/visual.html' },
            { type: 'track', id: 'experimentation', title: 'Data & Experimentation', description: 'Validate with synthetic data and testing', url: 'tracks/experimentation.html' },
            { type: 'track', id: 'storytelling', title: 'Storytelling & Presentation', description: 'Convince stakeholders with compelling demos', url: 'tracks/storytelling.html' },
            
            // Tools
            { type: 'tool', id: 'aider', title: 'Aider (AI Writing)', description: 'AI collaboration for documents and code', url: 'tools/aider.html' },
            { type: 'tool', id: 'workflows', title: 'Visual Workflows', description: 'n8n, Langflow, ToolJet automation', url: 'tools/workflows.html' },
            { type: 'tool', id: 'research-tools', title: 'Research Tools', description: 'Gemini CLI, OpenBB, competitive analysis', url: 'tools/research.html' },
            
            // Topics
            { type: 'topic', id: 'prompting', title: 'AI Prompting Techniques', description: 'Master effective AI communication', url: 'topics/prompting.html' },
            { type: 'topic', id: 'data-generation', title: 'Synthetic Data Generation', description: 'Create test data for validation', url: 'topics/data.html' },
        ];

        return content.filter(item => {
            const searchText = `${item.title} ${item.description}`.toLowerCase();
            return searchTerms.every(term => searchText.includes(term));
        });
    }

    displaySearchResults(results) {
        const container = document.querySelector('.search-results');
        
        if (results.length === 0) {
            container.innerHTML = '<p class="no-results">No results found. Try different keywords.</p>';
            return;
        }

        const html = results.map(result => `
            <div class="search-result" data-url="${result.url}">
                <div class="result-type">${result.type}</div>
                <h4>${result.title}</h4>
                <p>${result.description}</p>
            </div>
        `).join('');

        container.innerHTML = html;

        // Add click handlers
        container.querySelectorAll('.search-result').forEach(result => {
            result.addEventListener('click', (e) => {
                window.location.href = e.currentTarget.dataset.url;
            });
        });
    }

    updateProgress() {
        const totalTracks = 5;
        const completedTracks = Object.values(this.progress.tracks).filter(track => track.progress >= 100).length;
        const overallProgress = (completedTracks / totalTracks) * 100;

        // Update main progress bar
        const progressFill = document.querySelector('.progress-fill');
        const progressText = document.querySelector('.progress-text');
        
        progressFill.style.width = `${overallProgress}%`;
        
        if (overallProgress === 0) {
            progressText.textContent = 'Get started to track your progress';
        } else if (overallProgress === 100) {
            progressText.textContent = '🎉 All tracks completed! You\'re now AI-confident!';
        } else {
            progressText.textContent = `${Math.round(overallProgress)}% complete - ${completedTracks}/${totalTracks} tracks finished`;
        }

        // Update individual track progress
        document.querySelectorAll('.track-card').forEach(card => {
            const trackName = card.dataset.track;
            const trackProgress = this.progress.tracks[trackName];
            
            if (trackProgress) {
                const progressBar = card.querySelector('.progress-fill');
                const progressText = card.querySelector('.track-progress span');
                
                progressBar.style.width = `${trackProgress.progress}%`;
                
                if (trackProgress.progress === 0) {
                    progressText.textContent = 'Started';
                } else if (trackProgress.progress >= 100) {
                    progressText.textContent = '✅ Completed';
                } else {
                    progressText.textContent = `${Math.round(trackProgress.progress)}% complete`;
                }
            }
        });
    }

    loadRecentActivity() {
        const recentContainer = document.getElementById('recent-activity');
        const recentItems = this.getRecentActivity();

        if (recentItems.length === 0) {
            recentContainer.innerHTML = '<p class="empty-state">Start your first lesson to see your progress here</p>';
            return;
        }

        const html = recentItems.map(item => `
            <div class="recent-item">
                <div class="recent-icon">${item.icon}</div>
                <div class="recent-content">
                    <h4>${item.title}</h4>
                    <p>${item.description}</p>
                    <span class="recent-time">${item.timeAgo}</span>
                </div>
                <button class="recent-continue" data-url="${item.url}">Continue</button>
            </div>
        `).join('');

        recentContainer.innerHTML = html;

        // Add continue handlers
        recentContainer.querySelectorAll('.recent-continue').forEach(btn => {
            btn.addEventListener('click', (e) => {
                window.location.href = e.target.dataset.url;
            });
        });
    }

    getRecentActivity() {
        const activities = [];
        
        Object.entries(this.progress.tracks).forEach(([trackName, trackData]) => {
            if (trackData.started && trackData.progress < 100) {
                activities.push({
                    icon: this.getTrackIcon(trackName),
                    title: this.getTrackTitle(trackName),
                    description: `${Math.round(trackData.progress)}% complete`,
                    timeAgo: this.getTimeAgo(trackData.started),
                    url: `tracks/${trackName}.html`
                });
            }
        });

        return activities.sort((a, b) => new Date(b.started) - new Date(a.started)).slice(0, 3);
    }

    getTrackIcon(trackName) {
        const icons = {
            collaboration: '✍️',
            research: '🔍',
            visual: '🎨',
            experimentation: '🧪',
            storytelling: '🎬'
        };
        return icons[trackName] || '📚';
    }

    getTrackTitle(trackName) {
        const titles = {
            collaboration: 'AI Collaboration',
            research: 'Research & Analysis',
            visual: 'Visual Building',
            experimentation: 'Data & Experimentation',
            storytelling: 'Storytelling & Presentation'
        };
        return titles[trackName] || trackName;
    }

    getTimeAgo(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
        
        if (diffDays === 0) return 'Today';
        if (diffDays === 1) return 'Yesterday';
        return `${diffDays} days ago`;
    }

    showProgressModal() {
        // Create and show progress modal
        const modal = document.createElement('div');
        modal.className = 'progress-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <h3>Your Learning Progress</h3>
                <div class="progress-details">
                    ${this.generateProgressHTML()}
                </div>
                <button class="modal-close">Close</button>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        modal.querySelector('.modal-close').addEventListener('click', () => {
            modal.remove();
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.remove();
        });
    }

    generateProgressHTML() {
        const tracks = Object.entries(this.progress.tracks);
        
        if (tracks.length === 0) {
            return '<p>No progress yet. Start your first track to begin learning!</p>';
        }

        return tracks.map(([name, data]) => `
            <div class="progress-track">
                <div class="track-header">
                    <span>${this.getTrackIcon(name)} ${this.getTrackTitle(name)}</span>
                    <span>${Math.round(data.progress)}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${data.progress}%"></div>
                </div>
                <div class="track-stats">
                    Started: ${new Date(data.started).toLocaleDateString()}
                    • Modules: ${Object.keys(data.modules).length}
                </div>
            </div>
        `).join('');
    }

    loadProgress() {
        const stored = localStorage.getItem('aipm-learning-progress');
        return stored ? JSON.parse(stored) : {
            tracks: {},
            badges: [],
            totalTime: 0,
            lastActive: null
        };
    }

    saveProgress() {
        this.progress.lastActive = new Date().toISOString();
        localStorage.setItem('aipm-learning-progress', JSON.stringify(this.progress));
    }

    buildSearchIndex() {
        // Build search index for better performance
        // This could be expanded to include more sophisticated search
        this.searchIndex = {
            tracks: ['collaboration', 'research', 'visual', 'experimentation', 'storytelling'],
            tools: ['aider', 'workflows', 'research-tools', 'data-analysis'],
            topics: ['prompting', 'data-generation', 'automation', 'validation']
        };
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new LearningGuide();
});

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LearningGuide;
}