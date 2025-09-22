import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import { Button } from './ui/button';
import { Alert, AlertDescription, AlertTitle } from './ui/alert';

const ErrorMessage = ({ 
  title = "Something Went Wrong", 
  message = "We encountered an error while loading your data.", 
  onRetry,
  className = '' 
}) => {
  return (
    <div className={`flex justify-center items-center min-h-64 ${className}`}>
      <Alert className="max-w-md bg-slate-800 border-slate-700">
        <AlertTriangle className="h-4 w-4 text-yellow-500" />
        <AlertTitle className="text-white">{title}</AlertTitle>
        <AlertDescription className="text-slate-300 mt-2">
          {message}
        </AlertDescription>
        {onRetry && (
          <div className="mt-4">
            <Button 
              onClick={onRetry}
              variant="outline" 
              size="sm"
              className="border-slate-600 text-slate-300 hover:bg-slate-700"
            >
              <RefreshCw className="mr-2 h-4 w-4" />
              Try Again
            </Button>
          </div>
        )}
      </Alert>
    </div>
  );
};

export const ErrorSection = ({ title, error, onRetry, className = '' }) => {
  return (
    <section className={`py-20 ${className}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <ErrorMessage 
          title={`Error Loading ${title}`}
          message={error?.message || `Failed to load ${title.toLowerCase()} data. Please try again.`}
          onRetry={onRetry}
        />
      </div>
    </section>
  );
};

export default ErrorMessage;