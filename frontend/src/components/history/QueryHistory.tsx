import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { History, Search, Filter, Calendar, Clock, Tag, Users } from 'lucide-react';
import { Query, SEO_CATEGORIES, LLM_PROVIDERS } from '@/types/llm';
import { format } from 'date-fns';

interface QueryHistoryProps {
  onQuerySelect: (query: Query) => void;
  queries?: Query[];
  className?: string;
}

export const QueryHistory: React.FC<QueryHistoryProps> = ({ 
  onQuerySelect, 
  queries: providedQueries = [],
  className = '' 
}) => {
  const [queries, setQueries] = useState<Query[]>(providedQueries);
  const [filteredQueries, setFilteredQueries] = useState<Query[]>(providedQueries);
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [statusFilter, setStatusFilter] = useState<string>('all');

  // Update queries when providedQueries changes
  useEffect(() => {
    if (providedQueries.length === 0) {
      // Use mock data if no queries provided (for demonstration)
      const mockQueries: Query[] = [
        {
          id: 'q1',
          prompt: 'Best SEO practices for e-commerce websites in 2024',
          category: 'technical',
          tags: ['ecommerce', 'best-practices', '2024'],
          providers: ['openai', 'claude', 'perplexity'],
          created_at: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
          status: 'complete'
        },
        {
          id: 'q2', 
          prompt: 'Content strategy for local businesses targeting voice search',
          category: 'content',
          tags: ['local-seo', 'voice-search', 'content-strategy'],
          providers: ['openai', 'gemini'],
          created_at: new Date(Date.now() - 172800000).toISOString(), // 2 days ago
          status: 'complete'
        },
        {
          id: 'q3',
          prompt: 'Python script for automating meta description optimization',
          category: 'automation',
          tags: ['python', 'automation', 'meta-descriptions'],
          providers: ['claude', 'perplexity', 'gemini'],
          created_at: new Date(Date.now() - 259200000).toISOString(), // 3 days ago
          status: 'complete'
        }
      ];
      setQueries(mockQueries);
      setFilteredQueries(mockQueries);
    } else {
      setQueries(providedQueries);
      setFilteredQueries(providedQueries);
    }
  }, [providedQueries]);

  // Filter queries based on search and filters
  useEffect(() => {
    let filtered = queries;

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(query =>
        query.prompt.toLowerCase().includes(searchTerm.toLowerCase()) ||
        query.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Category filter
    if (categoryFilter !== 'all') {
      filtered = filtered.filter(query => query.category === categoryFilter);
    }

    // Status filter
    if (statusFilter !== 'all') {
      filtered = filtered.filter(query => query.status === statusFilter);
    }

    setFilteredQueries(filtered);
  }, [queries, searchTerm, categoryFilter, statusFilter]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'complete':
        return 'bg-status-complete text-white';
      case 'processing':
        return 'bg-status-processing text-white';
      case 'pending':
        return 'bg-status-pending text-white';
      case 'error':
        return 'bg-destructive text-destructive-foreground';
      default:
        return 'bg-muted text-muted-foreground';
    }
  };

  const getCategoryInfo = (category: string) => {
    return SEO_CATEGORIES.find(cat => cat.value === category);
  };

  return (
    <div className={`space-y-6 ${className}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <History className="h-6 w-6 text-primary" />
          <h2 className="text-2xl font-bold">Query History</h2>
        </div>
        <Badge variant="secondary" className="px-3 py-1">
          {filteredQueries.length} queries
        </Badge>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Filter className="h-5 w-5" />
            Filters
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Search */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search queries and tags..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>

            {/* Category Filter */}
            <Select value={categoryFilter} onValueChange={setCategoryFilter}>
              <SelectTrigger>
                <SelectValue placeholder="Filter by category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                {SEO_CATEGORIES.map(category => (
                  <SelectItem key={category.value} value={category.value}>
                    {category.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            {/* Status Filter */}
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger>
                <SelectValue placeholder="Filter by status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Statuses</SelectItem>
                <SelectItem value="complete">Complete</SelectItem>
                <SelectItem value="processing">Processing</SelectItem>
                <SelectItem value="pending">Pending</SelectItem>
                <SelectItem value="error">Error</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Query List */}
      <div className="space-y-4">
        {filteredQueries.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center">
              <div className="text-muted-foreground space-y-2">
                <History className="h-12 w-12 mx-auto opacity-50" />
                <p className="text-lg font-medium">No queries found</p>
                <p className="text-sm">
                  {queries.length === 0 
                    ? "You haven't submitted any queries yet"
                    : "Try adjusting your search or filters"
                  }
                </p>
              </div>
            </CardContent>
          </Card>
        ) : (
          filteredQueries.map((query, index) => {
            const categoryInfo = getCategoryInfo(query.category);
            
            return (
              <motion.div
                key={query.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="hover:shadow-md transition-all cursor-pointer border-2 hover:border-primary/20">
                  <CardContent className="p-6">
                    <div className="space-y-4">
                      {/* Header */}
                      <div className="flex items-start justify-between">
                        <div className="flex-1 space-y-2">
                          <p className="text-lg font-medium leading-tight">
                            {query.prompt}
                          </p>
                          <div className="flex items-center gap-4 text-sm text-muted-foreground">
                            <div className="flex items-center gap-1">
                              <Calendar className="h-4 w-4" />
                              {format(new Date(query.created_at), 'MMM d, yyyy')}
                            </div>
                            <div className="flex items-center gap-1">
                              <Clock className="h-4 w-4" />
                              {format(new Date(query.created_at), 'h:mm a')}
                            </div>
                          </div>
                        </div>
                        
                        <Badge className={getStatusColor(query.status)}>
                          {query.status.charAt(0).toUpperCase() + query.status.slice(1)}
                        </Badge>
                      </div>

                      {/* Metadata */}
                      <div className="space-y-3">
                        {/* Category */}
                        {categoryInfo && (
                          <div className="flex items-center gap-2">
                            <Badge variant="outline" className="text-xs">
                              {categoryInfo.label}
                            </Badge>
                            <span className="text-xs text-muted-foreground">
                              {categoryInfo.description}
                            </span>
                          </div>
                        )}

                        {/* Tags */}
                        {query.tags.length > 0 && (
                          <div className="flex items-center gap-2 flex-wrap">
                            <Tag className="h-4 w-4 text-muted-foreground" />
                            {query.tags.map(tag => (
                              <Badge key={tag} variant="secondary" className="text-xs">
                                {tag}
                              </Badge>
                            ))}
                          </div>
                        )}

                        {/* Providers */}
                        <div className="flex items-center gap-2 flex-wrap">
                          <Users className="h-4 w-4 text-muted-foreground" />
                          {query.providers.map(provider => {
                            const providerInfo = LLM_PROVIDERS[provider as keyof typeof LLM_PROVIDERS];
                            return (
                              <Badge 
                                key={provider} 
                                variant="outline" 
                                className="text-xs"
                              >
                                {providerInfo?.name || provider}
                              </Badge>
                            );
                          })}
                        </div>
                      </div>

                      {/* Actions */}
                      <div className="flex justify-end pt-2">
                        <Button
                          onClick={() => onQuerySelect(query)}
                          variant="outline"
                          size="sm"
                          disabled={query.status !== 'complete'}
                        >
                          {query.status === 'complete' ? 'View Results' : 'Not Available'}
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            );
          })
        )}
      </div>
    </div>
  );
};