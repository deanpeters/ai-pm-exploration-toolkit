/**
 * Track-specific functionality
 * Handles module progression, exercises, and progress tracking
 */

class TrackManager {
    constructor() {
        this.trackName = this.getTrackName();
        this.progress = this.loadTrackProgress();
        this.currentModule = null;
        
        this.init();
    }

    init() {
        this.setupModuleInteractions();
        this.setupCopyButtons();
        this.updateProgressDisplay();
        this.unlockAvailableModules();
    }

    getTrackName() {
        // Extract track name from URL
        const path = window.location.pathname;
        const match = path.match(/tracks\/([^.]+)\.html/);
        return match ? match[1] : 'unknown';
    }

    loadTrackProgress() {
        const stored = localStorage.getItem('aipm-learning-progress');
        const allProgress = stored ? JSON.parse(stored) : { tracks: {} };
        
        if (!allProgress.tracks[this.trackName]) {
            allProgress.tracks[this.trackName] = {
                started: new Date().toISOString(),
                modules: {},
                progress: 0
            };
        }
        
        return allProgress.tracks[this.trackName];
    }

    saveProgress() {
        const stored = localStorage.getItem('aipm-learning-progress');
        const allProgress = stored ? JSON.parse(stored) : { tracks: {} };
        
        allProgress.tracks[this.trackName] = this.progress;
        allProgress.lastActive = new Date().toISOString();
        
        localStorage.setItem('aipm-learning-progress', JSON.stringify(allProgress));
    }

    setupModuleInteractions() {
        // Module card clicks
        document.querySelectorAll('.module-card:not(.locked)').forEach(card => {
            const moduleHeader = card.querySelector('.module-header');
            moduleHeader.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleModule(card);
            });
        });

        // Exercise completion buttons
        document.querySelectorAll('.complete-exercise').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const module = e.target.dataset.module;
                this.completeModule(module);
            });
        });

        // Mastery path buttons
        document.querySelectorAll('.start-path').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const path = e.target.dataset.path;
                this.startMasteryPath(path);
            });
        });
    }

    setupCopyButtons() {
        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const codeBlock = e.target.nextElementSibling;
                const text = codeBlock.textContent;
                
                navigator.clipboard.writeText(text).then(() => {
                    e.target.textContent = 'Copied!';
                    e.target.classList.add('copied');
                    
                    setTimeout(() => {
                        e.target.textContent = 'Copy';
                        e.target.classList.remove('copied');
                    }, 2000);
                });
            });
        });
    }

    toggleModule(moduleCard) {
        const content = moduleCard.querySelector('.module-content');
        const isExpanded = !content.classList.contains('hidden');
        
        // Close all other modules
        document.querySelectorAll('.module-content').forEach(content => {
            content.classList.add('hidden');
        });
        
        // Toggle current module
        if (!isExpanded) {
            content.classList.remove('hidden');
            this.currentModule = moduleCard.dataset.module;
            
            // Track module start
            if (!this.progress.modules[this.currentModule]) {
                this.progress.modules[this.currentModule] = {
                    started: new Date().toISOString(),
                    completed: false,
                    timeSpent: 0
                };
                this.saveProgress();
            }
        } else {
            this.currentModule = null;
        }
    }

    completeModule(moduleName) {
        // Mark module as completed
        if (!this.progress.modules[moduleName]) {
            this.progress.modules[moduleName] = {
                started: new Date().toISOString(),
                completed: false,
                timeSpent: 0
            };
        }
        
        this.progress.modules[moduleName].completed = true;
        this.progress.modules[moduleName].completedAt = new Date().toISOString();
        
        // Update overall progress
        this.updateTrackProgress();
        
        // Update UI
        this.updateModuleStatus(moduleName, 'completed');
        this.unlockNextModule(moduleName);
        this.updateProgressDisplay();
        
        // Save progress
        this.saveProgress();
        
        // Show completion feedback
        this.showCompletionFeedback(moduleName);
    }

    updateTrackProgress() {
        const totalModules = 4; // learn, practice, apply, master
        const completedModules = Object.values(this.progress.modules)
            .filter(module => module.completed).length;
        
        this.progress.progress = (completedModules / totalModules) * 100;
    }

    updateModuleStatus(moduleName, status) {
        const moduleCard = document.querySelector(`[data-module="${moduleName}"]`);
        if (!moduleCard) return;
        
        const statusElement = moduleCard.querySelector('.module-status');
        
        switch (status) {
            case 'completed':
                statusElement.textContent = 'Completed';
                moduleCard.classList.add('completed');
                break;
            case 'in_progress':
                statusElement.textContent = 'In Progress';
                break;
            case 'locked':
                statusElement.textContent = 'Locked';
                moduleCard.classList.add('locked');
                break;
        }
    }

    unlockNextModule(completedModule) {
        const moduleOrder = ['learn', 'practice', 'apply', 'master'];
        const currentIndex = moduleOrder.indexOf(completedModule);
        
        if (currentIndex < moduleOrder.length - 1) {
            const nextModule = moduleOrder[currentIndex + 1];
            const nextCard = document.querySelector(`[data-module="${nextModule}"]`);
            
            if (nextCard && nextCard.classList.contains('locked')) {
                nextCard.classList.remove('locked');
                this.updateModuleStatus(nextModule, 'available');
                
                // Show unlock animation
                this.showUnlockAnimation(nextCard);
            }
        }
    }

    unlockAvailableModules() {
        const moduleOrder = ['learn', 'practice', 'apply', 'master'];
        
        // Always unlock the first module
        const firstCard = document.querySelector(`[data-module="${moduleOrder[0]}"]`);
        if (firstCard) {
            firstCard.classList.remove('locked');
        }
        
        // Unlock modules based on completed progress
        Object.keys(this.progress.modules).forEach(moduleName => {
            const moduleData = this.progress.modules[moduleName];
            const moduleIndex = moduleOrder.indexOf(moduleName);
            
            if (moduleData.completed) {
                this.updateModuleStatus(moduleName, 'completed');
                
                // Unlock next module
                if (moduleIndex < moduleOrder.length - 1) {
                    const nextModule = moduleOrder[moduleIndex + 1];
                    const nextCard = document.querySelector(`[data-module="${nextModule}"]`);
                    if (nextCard) {
                        nextCard.classList.remove('locked');
                    }
                }
            }
        });
    }

    updateProgressDisplay() {
        const progressFill = document.querySelector('.track-progress-header .progress-fill');
        const progressText = document.querySelector('.track-progress-header .progress-text');
        
        if (progressFill && progressText) {
            progressFill.style.width = `${this.progress.progress}%`;
            
            if (this.progress.progress === 0) {
                progressText.textContent = 'Get started';
            } else if (this.progress.progress >= 100) {
                progressText.textContent = '🎉 Track Complete!';
            } else {
                progressText.textContent = `${Math.round(this.progress.progress)}% Complete`;
            }
        }
    }

    showCompletionFeedback(moduleName) {
        // Create completion modal
        const modal = document.createElement('div');
        modal.className = 'completion-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="completion-icon">🎉</div>
                <h3>Module Completed!</h3>
                <p>Great job completing the ${this.getModuleTitle(moduleName)} module.</p>
                <div class="completion-stats">
                    <div class="stat">
                        <span class="stat-number">${Math.round(this.progress.progress)}%</span>
                        <span class="stat-label">Track Progress</span>
                    </div>
                    <div class="stat">
                        <span class="stat-number">${Object.keys(this.progress.modules).length}</span>
                        <span class="stat-label">Modules Started</span>
                    </div>
                </div>
                <button class="continue-btn">Continue Learning</button>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Auto-remove after 3 seconds or on click
        const continueBtn = modal.querySelector('.continue-btn');
        continueBtn.addEventListener('click', () => modal.remove());
        
        setTimeout(() => modal.remove(), 5000);
    }

    showUnlockAnimation(moduleCard) {
        moduleCard.style.transform = 'scale(1.05)';
        moduleCard.style.transition = 'transform 0.3s ease';
        
        setTimeout(() => {
            moduleCard.style.transform = 'scale(1)';
        }, 300);
        
        // Add unlock indicator
        const unlockIndicator = document.createElement('div');
        unlockIndicator.className = 'unlock-indicator';
        unlockIndicator.textContent = '🔓 Unlocked!';
        moduleCard.appendChild(unlockIndicator);
        
        setTimeout(() => unlockIndicator.remove(), 3000);
    }

    getModuleTitle(moduleName) {
        const titles = {
            learn: 'Learn',
            practice: 'Practice', 
            apply: 'Apply',
            master: 'Master'
        };
        return titles[moduleName] || moduleName;
    }

    startMasteryPath(pathName) {
        // Navigate to mastery path or show selection
        alert(`Starting ${pathName} mastery path - this would navigate to advanced content`);
    }
}

// Additional CSS for modals and animations
const additionalCSS = `
.completion-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0; 
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    animation: modalFadeIn 0.3s ease;
}

.completion-modal .modal-content {
    background: white;
    border-radius: var(--radius-lg);
    padding: var(--space-8);
    text-align: center;
    max-width: 400px;
    margin: var(--space-4);
    animation: modalSlideUp 0.3s ease;
}

.completion-icon {
    font-size: 3rem;
    margin-bottom: var(--space-4);
}

.completion-stats {
    display: flex;
    gap: var(--space-6);
    justify-content: center;
    margin: var(--space-6) 0;
}

.stat {
    text-align: center;
}

.stat-number {
    display: block;
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary);
}

.stat-label {
    font-size: 0.875rem;
    color: var(--gray-500);
}

.continue-btn {
    background: var(--primary);
    color: white;
    border: none;
    padding: var(--space-3) var(--space-6);
    border-radius: var(--radius);
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.2s;
}

.continue-btn:hover {
    background: var(--primary-dark);
}

.unlock-indicator {
    position: absolute;
    top: var(--space-2);
    right: var(--space-2);
    background: var(--success);
    color: white;
    padding: var(--space-1) var(--space-2);
    border-radius: var(--radius);
    font-size: 0.75rem;
    font-weight: 500;
    animation: unlockPulse 2s ease-in-out;
}

@keyframes modalFadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes modalSlideUp {
    from { transform: translateY(50px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

@keyframes unlockPulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}
`;

// Inject additional CSS
const style = document.createElement('style');
style.textContent = additionalCSS;
document.head.appendChild(style);

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TrackManager();
});

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TrackManager;
}