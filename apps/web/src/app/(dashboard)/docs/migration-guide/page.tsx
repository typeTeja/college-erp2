import { Metadata } from 'next';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowRight, MapPin } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Migration Guide - College ERP',
  description: 'Find where your favorite features moved',
};

export default function MigrationGuidePage() {
  const migrations = [
    {
      category: 'Institutional Setup',
      items: [
        { old: 'Settings → Institutional Setup', new: 'Setup → Institutional Setup' },
        { old: 'Settings → Basic Information', new: 'Setup → Institutional Setup → Basic Info' },
        { old: 'Settings → Contact Details', new: 'Setup → Institutional Setup → Contact' },
      ],
    },
    {
      category: 'Academic Configuration',
      items: [
        { old: 'Settings → Academic Configuration', new: 'Config → Academic' },
        { old: 'Settings → Departments', new: 'Config → Academic → Departments' },
        { old: 'Settings → Programs', new: 'Config → Academic → Programs' },
        { old: 'Settings → Courses', new: 'Config → Academic → Courses' },
        { old: 'Settings → Academic Calendar', new: 'Config → Academic → Calendar' },
      ],
    },
    {
      category: 'Finance Configuration',
      items: [
        { old: 'Settings → Finance Configuration', new: 'Config → Finance' },
        { old: 'Settings → Fee Structure', new: 'Config → Finance → Fee Structure' },
        { old: 'Settings → Fee Categories', new: 'Config → Finance → Categories' },
        { old: 'Settings → Payment Methods', new: 'Config → Finance → Payment Methods' },
      ],
    },
    {
      category: 'Admission Setup',
      items: [
        { old: 'Settings → Admission Setup', new: 'Config → Admission' },
        { old: 'Settings → Admission Criteria', new: 'Config → Admission → Criteria' },
        { old: 'Settings → Application Form', new: 'Config → Admission → Form Builder' },
      ],
    },
    {
      category: 'System Administration',
      items: [
        { old: 'Settings → User Management', new: 'System → Users' },
        { old: 'Settings → Role Management', new: 'System → Roles & Permissions' },
        { old: 'Settings → Integrations', new: 'System → Integrations' },
        { old: 'Settings → Audit Logs', new: 'System → Audit Logs' },
      ],
    },
    {
      category: 'Personal Settings',
      items: [
        { old: 'Settings → Profile', new: 'Profile Menu → My Profile' },
        { old: 'Settings → Change Password', new: 'Profile Menu → Security' },
        { old: 'Settings → Preferences', new: 'Profile Menu → Preferences' },
        { old: 'Settings → Notifications', new: 'Profile Menu → Notifications' },
      ],
    },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center space-y-4">
        <div className="flex items-center justify-center gap-2">
          <MapPin className="h-8 w-8 text-purple-600" />
          <h1 className="text-4xl font-bold">Migration Guide</h1>
        </div>
        <p className="text-lg text-muted-foreground">
          Find where your favorite features moved
        </p>
      </div>

      {/* Quick Tip */}
      <Card className="bg-blue-50 dark:bg-blue-950 border-blue-200 dark:border-blue-800">
        <CardHeader>
          <CardTitle className="text-blue-900 dark:text-blue-100 text-base">💡 Quick Tip</CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-blue-800 dark:text-blue-200">
          <p>
            Can't find something? Press <kbd className="px-2 py-1 bg-blue-100 dark:bg-blue-900 rounded text-xs font-mono">⌘K</kbd> or <kbd className="px-2 py-1 bg-blue-100 dark:bg-blue-900 rounded text-xs font-mono">Ctrl+K</kbd> to open the command palette and search for any page.
          </p>
        </CardContent>
      </Card>

      {/* Migration Tables */}
      {migrations.map((section) => (
        <Card key={section.category}>
          <CardHeader>
            <CardTitle>{section.category}</CardTitle>
            <CardDescription>
              Updated locations for {section.category.toLowerCase()}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {section.items.map((item, index) => (
                <div
                  key={index}
                  className="flex items-center gap-3 p-3 rounded-lg bg-slate-50 dark:bg-slate-900"
                >
                  <div className="flex-1 text-sm">
                    <div className="text-muted-foreground">{item.old}</div>
                  </div>
                  <ArrowRight className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                  <div className="flex-1 text-sm">
                    <div className="font-semibold text-green-600 dark:text-green-400">
                      {item.new}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      ))}

      {/* Redirects Notice */}
      <Card className="bg-green-50 dark:bg-green-950 border-green-200 dark:border-green-800">
        <CardHeader>
          <CardTitle className="text-green-900 dark:text-green-100 text-base">
            ✓ Automatic Redirects
          </CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-green-800 dark:text-green-200">
          <p>
            All old URLs automatically redirect to the new locations. Your bookmarks will continue to work!
          </p>
        </CardContent>
      </Card>

      {/* Help */}
      <Card>
        <CardHeader>
          <CardTitle>Still Can't Find Something?</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          <p className="text-muted-foreground">
            We're here to help:
          </p>
          <ul className="space-y-1 text-muted-foreground">
            <li>
              <a href="/docs/faq" className="text-blue-600 hover:underline">
                Check the FAQ
              </a>
            </li>
            <li>
              <a href="/docs/whats-new" className="text-blue-600 hover:underline">
                See what's new
              </a>
            </li>
            <li>
              Contact support: <a href="mailto:support@college-erp.com" className="text-blue-600 hover:underline">support@college-erp.com</a>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
