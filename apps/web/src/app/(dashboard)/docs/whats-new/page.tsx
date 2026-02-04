import { Metadata } from 'next';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Sparkles, Navigation, LayoutDashboard, Zap, Smartphone, Search } from 'lucide-react';

export const metadata: Metadata = {
  title: "What's New - College ERP",
  description: 'Discover the latest improvements to navigation and dashboards',
};

export default function WhatsNewPage() {
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center space-y-4">
        <div className="flex items-center justify-center gap-2">
          <Sparkles className="h-8 w-8 text-blue-600" />
          <h1 className="text-4xl font-bold">What's New</h1>
        </div>
        <p className="text-lg text-muted-foreground">
          We've redesigned the navigation and dashboards for a better experience
        </p>
        <Badge variant="outline" className="text-sm">
          Released: February 2026
        </Badge>
      </div>

      {/* Navigation Changes */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Navigation className="h-5 w-5 text-blue-600" />
            <CardTitle>New Navigation Structure</CardTitle>
          </div>
          <CardDescription>
            Simplified 4-layer navigation for faster access
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <h3 className="font-semibold mb-2">Key Improvements:</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li className="flex items-start gap-2">
                <span className="text-green-600 mt-1">✓</span>
                <span><strong>4-Layer Structure:</strong> Setup → Config → System → Profile for logical grouping</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-600 mt-1">✓</span>
                <span><strong>Profile Menu:</strong> Personal settings moved to top-right dropdown</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-600 mt-1">✓</span>
                <span><strong>Collapsible Sidebar:</strong> More screen space when you need it</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-600 mt-1">✓</span>
                <span><strong>Breadcrumbs:</strong> Always know where you are</span>
              </li>
            </ul>
          </div>

          <div className="bg-slate-50 dark:bg-slate-900 p-4 rounded-lg">
            <h4 className="font-semibold text-sm mb-2">Navigation Layers:</h4>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-sm">
              <div className="space-y-1">
                <div className="font-semibold text-blue-600">Setup</div>
                <div className="text-xs text-muted-foreground">Initial configuration</div>
              </div>
              <div className="space-y-1">
                <div className="font-semibold text-purple-600">Config</div>
                <div className="text-xs text-muted-foreground">Domain settings</div>
              </div>
              <div className="space-y-1">
                <div className="font-semibold text-orange-600">System</div>
                <div className="text-xs text-muted-foreground">Administration</div>
              </div>
              <div className="space-y-1">
                <div className="font-semibold text-green-600">Profile</div>
                <div className="text-xs text-muted-foreground">Personal settings</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Command Palette */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Search className="h-5 w-5 text-purple-600" />
            <CardTitle>Command Palette</CardTitle>
          </div>
          <CardDescription>
            Quick navigation with keyboard shortcuts
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-muted-foreground">
            Press <kbd className="px-2 py-1 bg-slate-100 dark:bg-slate-800 rounded text-xs font-mono">⌘K</kbd> or <kbd className="px-2 py-1 bg-slate-100 dark:bg-slate-800 rounded text-xs font-mono">Ctrl+K</kbd> to open the command palette and search for any page.
          </p>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li className="flex items-start gap-2">
              <span className="text-green-600 mt-1">✓</span>
              <span>Search all pages and settings</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-600 mt-1">✓</span>
              <span>Keyboard navigation with arrow keys</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-600 mt-1">✓</span>
              <span>Recent pages for quick access</span>
            </li>
          </ul>
        </CardContent>
      </Card>

      {/* Dashboard Improvements */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <LayoutDashboard className="h-5 w-5 text-orange-600" />
            <CardTitle>Role-Specific Dashboards</CardTitle>
          </div>
          <CardDescription>
            Tailored dashboards for every role
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <h3 className="font-semibold mb-2">New Dashboards:</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div className="bg-blue-50 dark:bg-blue-950 p-3 rounded-lg">
                <div className="font-semibold text-sm text-blue-900 dark:text-blue-100">Principal Dashboard</div>
                <div className="text-xs text-blue-700 dark:text-blue-300 mt-1">
                  Institutional health, enrollment trends, financial overview
                </div>
              </div>
              <div className="bg-green-50 dark:bg-green-950 p-3 rounded-lg">
                <div className="font-semibold text-sm text-green-900 dark:text-green-100">Parent Dashboard</div>
                <div className="text-xs text-green-700 dark:text-green-300 mt-1">
                  Student progress, attendance, fees, announcements
                </div>
              </div>
              <div className="bg-purple-50 dark:bg-purple-950 p-3 rounded-lg">
                <div className="font-semibold text-sm text-purple-900 dark:text-purple-100">Student Dashboard</div>
                <div className="text-xs text-purple-700 dark:text-purple-300 mt-1">
                  Timetable, attendance, assignments, exam schedule
                </div>
              </div>
              <div className="bg-orange-50 dark:bg-orange-950 p-3 rounded-lg">
                <div className="font-semibold text-sm text-orange-900 dark:text-orange-100">Staff Dashboard</div>
                <div className="text-xs text-orange-700 dark:text-orange-300 mt-1">
                  Role-based views for Librarian, Warden, Accounts, SSE
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Performance */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Zap className="h-5 w-5 text-yellow-600" />
            <CardTitle>Performance Improvements</CardTitle>
          </div>
          <CardDescription>
            Faster page loads and smoother interactions
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li className="flex items-start gap-2">
              <span className="text-green-600 mt-1">✓</span>
              <span>50% faster page load times</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-600 mt-1">✓</span>
              <span>Optimized dashboard data fetching</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-600 mt-1">✓</span>
              <span>Reduced bundle size</span>
            </li>
          </ul>
        </CardContent>
      </Card>

      {/* Mobile */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Smartphone className="h-5 w-5 text-green-600" />
            <CardTitle>Mobile Responsive</CardTitle>
          </div>
          <CardDescription>
            Optimized for all devices
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li className="flex items-start gap-2">
              <span className="text-green-600 mt-1">✓</span>
              <span>Mobile-optimized navigation</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-600 mt-1">✓</span>
              <span>Bottom navigation bar on mobile</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-600 mt-1">✓</span>
              <span>Touch-friendly interactions</span>
            </li>
          </ul>
        </CardContent>
      </Card>

      {/* Next Steps */}
      <Card className="bg-blue-50 dark:bg-blue-950 border-blue-200 dark:border-blue-800">
        <CardHeader>
          <CardTitle className="text-blue-900 dark:text-blue-100">Need Help?</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          <p className="text-blue-800 dark:text-blue-200">
            Check out our other resources:
          </p>
          <ul className="space-y-1 text-blue-700 dark:text-blue-300">
            <li>
              <a href="/docs/migration-guide" className="underline hover:text-blue-900 dark:hover:text-blue-100">
                Migration Guide - Where did X go?
              </a>
            </li>
            <li>
              <a href="/docs/faq" className="underline hover:text-blue-900 dark:hover:text-blue-100">
                FAQ - Common questions
              </a>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
