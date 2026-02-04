import { Metadata } from 'next';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { HelpCircle } from 'lucide-react';

export const metadata: Metadata = {
  title: 'FAQ - College ERP',
  description: 'Frequently asked questions about the new navigation and dashboards',
};

export default function FAQPage() {
  const faqs = [
    {
      category: 'Navigation',
      questions: [
        {
          q: 'Where did the settings page go?',
          a: 'Settings have been reorganized into logical groups: Setup (institutional), Config (domain settings), System (administration), and Profile (personal settings). Use the command palette (⌘K) to quickly find what you need.',
        },
        {
          q: 'How do I access institutional setup?',
          a: 'Click "Setup" in the sidebar, then "Institutional Setup". Or press ⌘K and search for "institutional".',
        },
        {
          q: 'What happened to my dashboard?',
          a: 'We\'ve created role-specific dashboards! You\'ll see a dashboard tailored to your role (Principal, Parent, Student, Staff, or Faculty) with relevant widgets and information.',
        },
        {
          q: 'How do I use the command palette?',
          a: 'Press ⌘K (Mac) or Ctrl+K (Windows/Linux) to open the command palette. Type to search for any page, then press Enter to navigate. Use arrow keys to navigate results.',
        },
        {
          q: 'Can I switch back to the old navigation?',
          a: 'The new navigation is now the default for all users. We believe it provides a better experience, but if you have specific concerns, please contact support.',
        },
        {
          q: 'Why can\'t I see certain menu items?',
          a: 'Menu items are filtered based on your role and permissions. If you believe you should have access to something, contact your administrator.',
        },
      ],
    },
    {
      category: 'Dashboards',
      questions: [
        {
          q: 'How do I access the new dashboards?',
          a: 'Click "Dashboard" in the sidebar or press ⌘K and search for "dashboard". You\'ll see a dashboard specific to your role.',
        },
        {
          q: 'What widgets are available on my dashboard?',
          a: 'Each role has different widgets. For example, the Principal dashboard shows enrollment trends and financial overview, while the Student dashboard shows timetable and assignments.',
        },
        {
          q: 'Can I customize my dashboard?',
          a: 'Dashboard widgets are currently fixed based on your role to ensure consistency. Custom dashboards may be available in a future update.',
        },
        {
          q: 'Why is my dashboard loading slowly?',
          a: 'Dashboards fetch real-time data, which may take a moment. We\'ve optimized performance, but if you continue to experience slow loading, please contact support.',
        },
      ],
    },
    {
      category: 'Features',
      questions: [
        {
          q: 'What are the keyboard shortcuts?',
          a: '⌘K or Ctrl+K opens the command palette. Use arrow keys to navigate, Enter to select, and Esc to close.',
        },
        {
          q: 'Is the new interface mobile-friendly?',
          a: 'Yes! The new navigation includes a mobile-optimized bottom navigation bar and touch-friendly interactions.',
        },
        {
          q: 'How do I collapse the sidebar?',
          a: 'Click the collapse icon in the sidebar header to toggle between expanded and collapsed states. Your preference is saved automatically.',
        },
        {
          q: 'What are breadcrumbs?',
          a: 'Breadcrumbs show your current location in the navigation hierarchy. Click any breadcrumb to navigate back to that level.',
        },
      ],
    },
    {
      category: 'Troubleshooting',
      questions: [
        {
          q: 'I\'m getting a 404 error on an old URL',
          a: 'Old URLs should automatically redirect to new locations. If you\'re still getting a 404, try using the command palette (⌘K) to search for the page, or check the Migration Guide.',
        },
        {
          q: 'The command palette isn\'t opening',
          a: 'Make sure you\'re using the correct shortcut: ⌘K on Mac, Ctrl+K on Windows/Linux. If it still doesn\'t work, try refreshing the page.',
        },
        {
          q: 'My sidebar is stuck collapsed/expanded',
          a: 'Try clicking the collapse icon in the sidebar header. If that doesn\'t work, clear your browser\'s localStorage and refresh.',
        },
        {
          q: 'I can\'t find a specific setting',
          a: 'Use the command palette (⌘K) to search for it, or check the Migration Guide to see where it moved.',
        },
      ],
    },
    {
      category: 'Feedback',
      questions: [
        {
          q: 'How do I report a bug?',
          a: 'Click the feedback button in the bottom-right corner, select "Bug Report", and describe the issue. You can also email support@college-erp.com.',
        },
        {
          q: 'How do I request a new feature?',
          a: 'Click the feedback button in the bottom-right corner, select "Feature Request", and describe your idea. We review all feedback!',
        },
        {
          q: 'Who do I contact for help?',
          a: 'For technical support, email support@college-erp.com. For account or permission issues, contact your institution\'s administrator.',
        },
      ],
    },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center space-y-4">
        <div className="flex items-center justify-center gap-2">
          <HelpCircle className="h-8 w-8 text-green-600" />
          <h1 className="text-4xl font-bold">Frequently Asked Questions</h1>
        </div>
        <p className="text-lg text-muted-foreground">
          Common questions about the new navigation and dashboards
        </p>
      </div>

      {/* Quick Search Tip */}
      <Card className="bg-blue-50 dark:bg-blue-950 border-blue-200 dark:border-blue-800">
        <CardHeader>
          <CardTitle className="text-blue-900 dark:text-blue-100 text-base">💡 Quick Tip</CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-blue-800 dark:text-blue-200">
          <p>
            Use <kbd className="px-2 py-1 bg-blue-100 dark:bg-blue-900 rounded text-xs font-mono">⌘F</kbd> or <kbd className="px-2 py-1 bg-blue-100 dark:bg-blue-900 rounded text-xs font-mono">Ctrl+F</kbd> to search this page for specific questions.
          </p>
        </CardContent>
      </Card>

      {/* FAQ Sections */}
      {faqs.map((section) => (
        <Card key={section.category}>
          <CardHeader>
            <CardTitle>{section.category}</CardTitle>
            <CardDescription>
              {section.questions.length} questions
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Accordion type="single" collapsible className="w-full">
              {section.questions.map((faq, index) => (
                <AccordionItem key={index} value={`item-${index}`}>
                  <AccordionTrigger className="text-left">
                    {faq.q}
                  </AccordionTrigger>
                  <AccordionContent className="text-muted-foreground">
                    {faq.a}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </CardContent>
        </Card>
      ))}

      {/* Still Need Help */}
      <Card className="bg-green-50 dark:bg-green-950 border-green-200 dark:border-green-800">
        <CardHeader>
          <CardTitle className="text-green-900 dark:text-green-100">Still Need Help?</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm text-green-800 dark:text-green-200">
          <p>We're here to help:</p>
          <ul className="space-y-1">
            <li>
              <a href="/docs/whats-new" className="underline hover:text-green-900 dark:hover:text-green-100">
                See what's new
              </a>
            </li>
            <li>
              <a href="/docs/migration-guide" className="underline hover:text-green-900 dark:hover:text-green-100">
                Check the migration guide
              </a>
            </li>
            <li>
              Email: <a href="mailto:support@college-erp.com" className="underline hover:text-green-900 dark:hover:text-green-100">support@college-erp.com</a>
            </li>
            <li>
              Use the feedback widget (bottom-right corner)
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
