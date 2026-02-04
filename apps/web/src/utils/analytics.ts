/**
 * Analytics Utility
 * 
 * Centralized analytics tracking for user behavior and feature usage.
 * Supports PostHog, Mixpanel, Google Analytics, or custom providers.
 */

interface AnalyticsEvent {
  event: string;
  properties?: Record<string, any>;
}

interface PageViewEvent {
  name: string;
  properties?: Record<string, any>;
}

class Analytics {
  private isInitialized = false;

  /**
   * Initialize analytics provider
   * Call this once in _app.tsx or layout.tsx
   */
  init() {
    if (typeof window === 'undefined') return;
    
    // TODO: Initialize your analytics provider here
    // Example for PostHog:
    // posthog.init('YOUR_API_KEY', { api_host: 'https://app.posthog.com' });
    
    this.isInitialized = true;
  }

  /**
   * Track a custom event
   * 
   * @example
   * ```ts
   * analytics.track('navigation_click', {
   *   from: 'sidebar',
   *   to: '/setup/institutional',
   *   userId: user.id,
   * });
   * ```
   */
  track(event: string, properties?: Record<string, any>) {
    if (typeof window === 'undefined' || !this.isInitialized) return;

    try {
      // TODO: Replace with your analytics provider
      // Example for PostHog:
      // posthog.capture(event, properties);
      
      // Example for Mixpanel:
      // mixpanel.track(event, properties);
      
      // Example for Google Analytics:
      // gtag('event', event, properties);
      
      // Development logging
      if (process.env.NODE_ENV === 'development') {
        console.log('[Analytics]', event, properties);
      }
    } catch (error) {
      console.error('[Analytics] Track error:', error);
    }
  }

  /**
   * Track a page view
   * 
   * @example
   * ```ts
   * analytics.page('Principal Dashboard', {
   *   path: '/principal',
   *   userId: user.id,
   * });
   * ```
   */
  page(name: string, properties?: Record<string, any>) {
    if (typeof window === 'undefined' || !this.isInitialized) return;

    try {
      // TODO: Replace with your analytics provider
      // Example for PostHog:
      // posthog.capture('$pageview', { ...properties, page: name });
      
      // Example for Mixpanel:
      // mixpanel.track_pageview({ ...properties, page: name });
      
      // Example for Google Analytics:
      // gtag('event', 'page_view', { page_title: name, ...properties });
      
      // Development logging
      if (process.env.NODE_ENV === 'development') {
        console.log('[Analytics] Page view:', name, properties);
      }
    } catch (error) {
      console.error('[Analytics] Page error:', error);
    }
  }

  /**
   * Identify a user
   * 
   * @example
   * ```ts
   * analytics.identify(user.id, {
   *   email: user.email,
   *   role: user.role,
   * });
   * ```
   */
  identify(userId: string | number, traits?: Record<string, any>) {
    if (typeof window === 'undefined' || !this.isInitialized) return;

    try {
      // TODO: Replace with your analytics provider
      // Example for PostHog:
      // posthog.identify(userId.toString(), traits);
      
      // Example for Mixpanel:
      // mixpanel.identify(userId.toString());
      // mixpanel.people.set(traits);
      
      // Development logging
      if (process.env.NODE_ENV === 'development') {
        console.log('[Analytics] Identify:', userId, traits);
      }
    } catch (error) {
      console.error('[Analytics] Identify error:', error);
    }
  }

  /**
   * Reset analytics (on logout)
   */
  reset() {
    if (typeof window === 'undefined' || !this.isInitialized) return;

    try {
      // TODO: Replace with your analytics provider
      // Example for PostHog:
      // posthog.reset();
      
      // Example for Mixpanel:
      // mixpanel.reset();
      
      // Development logging
      if (process.env.NODE_ENV === 'development') {
        console.log('[Analytics] Reset');
      }
    } catch (error) {
      console.error('[Analytics] Reset error:', error);
    }
  }
}

// Export singleton instance
export const analytics = new Analytics();

/**
 * Predefined event tracking functions
 */
export const trackNavigationClick = (from: string, to: string, userId: number) => {
  analytics.track('navigation_click', { from, to, userId });
};

export const trackDashboardView = (dashboard: string, userId: number, role: string) => {
  analytics.track('dashboard_view', { dashboard, userId, role });
};

export const trackWidgetInteraction = (
  dashboard: string,
  widget: string,
  action: string,
  userId: number
) => {
  analytics.track('widget_interaction', { dashboard, widget, action, userId });
};

export const trackCommandPaletteSearch = (
  query: string,
  resultClicked: string | null,
  userId: number
) => {
  analytics.track('command_palette_search', { query, resultClicked, userId });
};

export const trackFeedbackSubmission = (
  rating: string | null,
  category: string,
  userId: number
) => {
  analytics.track('feedback_submission', { rating, category, userId });
};

export const trackPageView = (path: string, userId?: number) => {
  analytics.page(path, { path, userId });
};
