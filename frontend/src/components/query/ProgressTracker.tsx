import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { CheckCircle, Clock, Loader2, Brain, BarChart3 } from 'lucide-react';
import { ProgressUpdate, LLM_PROVIDERS } from '@/types/llm';
import { createProgressWebSocket } from '@/services/api';

interface ProgressTrackerProps {
  queryId: string;
  providers: string[];
  onComplete: () => void;
}

export const ProgressTracker: React.FC<ProgressTrackerProps> = ({ 
  queryId, 
  providers, 
  onComplete 
}) => {
  const [progress, setProgress] = useState<ProgressUpdate>({
    status: 'processing',
    completed_providers: [],
    total_providers: providers.length,
    message: 'Initializing queries...',
    progress_percentage: 0
  });

  const [startTime] = useState(Date.now());
  const [elapsedTime, setElapsedTime] = useState(0);

  useEffect(() => {
    // Create WebSocket connection for real-time updates
    const progressWS = createProgressWebSocket(queryId, (update) => {
      setProgress(update);
      if (update.status === 'complete') {
        onComplete();
      }
    });

    progressWS.connect();

    // Update elapsed time every second
    const timer = setInterval(() => {
      setElapsedTime(Math.floor((Date.now() - startTime) / 1000));
    }, 1000);

    return () => {
      progressWS.disconnect();
      clearInterval(timer);
    };
  }, [queryId, onComplete, startTime]);

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getProviderStatus = (provider: string) => {
    if (progress.completed_providers.includes(provider)) {
      return 'complete';
    }
    if (progress.status === 'processing' && 
        progress.completed_providers.length < providers.indexOf(provider) + 1) {
      return 'pending';
    }
    return 'processing';
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'complete':
        return <CheckCircle className="h-5 w-5 text-status-complete" />;
      case 'processing':
        return <Loader2 className="h-5 w-5 text-status-processing animate-spin" />;
      default:
        return <Clock className="h-5 w-5 text-status-pending" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'complete':
        return 'bg-status-complete text-white';
      case 'processing':
        return 'bg-status-processing text-white';
      default:
        return 'bg-status-pending text-white';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-4xl mx-auto"
    >
      <Card className="shadow-elevated">
        <CardHeader className="text-center pb-6">
          <CardTitle className="text-2xl font-bold flex items-center justify-center gap-3">
            <Brain className="h-6 w-6 text-primary animate-pulse-slow" />
            LLM Analysis in Progress
          </CardTitle>
          <CardDescription className="text-base">
            Querying {providers.length} AI models and analyzing responses for insights
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-8">
          {/* Overall Progress */}
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-lg font-medium">{progress.message}</span>
              <div className="text-right">
                <div className="text-2xl font-bold text-primary">
                  {progress.progress_percentage}%
                </div>
                <div className="text-sm text-muted-foreground">
                  {formatTime(elapsedTime)} elapsed
                </div>
              </div>
            </div>
            
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: '100%' }}
              transition={{ duration: 0.5 }}
            >
              <Progress 
                value={progress.progress_percentage} 
                className="h-3"
              />
            </motion.div>
          </div>

          {/* Provider Status Grid */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium flex items-center gap-2">
              <BarChart3 className="h-5 w-5" />
              Provider Status
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <AnimatePresence>
                {providers.map((provider, index) => {
                  const providerInfo = LLM_PROVIDERS[provider as keyof typeof LLM_PROVIDERS];
                  const status = getProviderStatus(provider);
                  
                  return (
                    <motion.div
                      key={provider}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <Card className={`transition-all border-2 ${
                        status === 'complete' 
                          ? 'border-status-complete bg-status-complete/5'
                          : status === 'processing'
                          ? 'border-status-processing bg-status-processing/5'
                          : 'border-border'
                      }`}>
                        <CardContent className="p-4">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              {getStatusIcon(status)}
                              <div>
                                <div className="font-medium">
                                  {providerInfo?.name || provider}
                                </div>
                                <div className="text-sm text-muted-foreground">
                                  {status === 'complete' && '✓ Response received'}
                                  {status === 'processing' && '⏳ Processing...'}
                                  {status === 'pending' && '⏸ Waiting in queue'}
                                </div>
                              </div>
                            </div>
                            
                            <Badge className={getStatusColor(status)}>
                              {status.charAt(0).toUpperCase() + status.slice(1)}
                            </Badge>
                          </div>
                        </CardContent>
                      </Card>
                    </motion.div>
                  );
                })}
              </AnimatePresence>
            </div>
          </div>

          {/* Analysis Phase Indicator */}
          {progress.status === 'analyzing' && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="p-6 bg-gradient-to-r from-primary/10 to-accent/10 rounded-lg border border-primary/20"
            >
              <div className="flex items-center justify-center space-x-3">
                <BarChart3 className="h-6 w-6 text-primary animate-pulse-slow" />
                <div className="text-center">
                  <div className="text-lg font-medium">Analyzing Responses</div>
                  <div className="text-sm text-muted-foreground">
                    Computing similarity scores, extracting insights, and preparing comparisons...
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {/* Estimated Completion */}
          <div className="text-center p-4 bg-muted/30 rounded-lg">
            <div className="text-sm text-muted-foreground">
              <span className="font-medium">Estimated completion:</span> Usually takes 30-45 seconds
            </div>
            <div className="text-xs text-muted-foreground mt-1">
              Processing time varies based on response complexity and provider load
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};