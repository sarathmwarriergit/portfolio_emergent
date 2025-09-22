import React from 'react';

const LoadingSpinner = ({ size = 'md', className = '' }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8', 
    lg: 'w-12 h-12',
    xl: 'w-16 h-16'
  };

  return (
    <div className={`flex justify-center items-center ${className}`}>
      <div 
        className={`${sizeClasses[size]} border-4 border-slate-600 border-t-blue-400 rounded-full animate-spin`}
      />
    </div>
  );
};

export const SkeletonCard = ({ className = '' }) => {
  return (
    <div className={`animate-pulse ${className}`}>
      <div className="bg-slate-700 rounded-lg p-6">
        <div className="h-4 bg-slate-600 rounded w-3/4 mb-3"></div>
        <div className="space-y-2">
          <div className="h-3 bg-slate-600 rounded w-full"></div>
          <div className="h-3 bg-slate-600 rounded w-2/3"></div>
        </div>
      </div>
    </div>
  );
};

export const SkeletonSection = ({ title, cardCount = 3, className = '' }) => {
  return (
    <section className={`py-20 ${className}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <div className="h-8 bg-slate-700 rounded w-48 mx-auto mb-4 animate-pulse"></div>
          <div className="w-20 h-1 bg-slate-600 mx-auto animate-pulse"></div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {Array.from({ length: cardCount }).map((_, index) => (
            <SkeletonCard key={index} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default LoadingSpinner;