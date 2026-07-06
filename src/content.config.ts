import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const reviews = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/reviews' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.date(),
    author: z.string().default('AI Tools Team'),
    category: z.string().default('review'),
    rating: z.number().min(1).max(5),
    product: z.string(),
    pricing: z.string().optional(),
    pros: z.array(z.string()).default([]),
    cons: z.array(z.string()).default([]),
    image: z.string().optional(),
    featured: z.boolean().default(false),
    tags: z.array(z.string()).default([]),
    affiliate_link: z.string().url().optional(),
  }),
});

const comparisons = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/comparisons' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.date(),
    author: z.string().default('AI Tools Team'),
    category: z.string().default('comparison'),
    products: z.array(z.string()),
    winner: z.string().optional(),
    image: z.string().optional(),
    featured: z.boolean().default(false),
    tags: z.array(z.string()).default([]),
    affiliate_links: z.record(z.string()).default({}),
  }),
});

const alternatives = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/alternatives' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.date(),
    author: z.string().default('AI Tools Team'),
    category: z.string().default('alternatives'),
    original_product: z.string(),
    alternatives_list: z.array(z.object({
      name: z.string(),
      description: z.string(),
      rating: z.number().min(1).max(5).optional(),
    })),
    image: z.string().optional(),
    featured: z.boolean().default(false),
    tags: z.array(z.string()).default([]),
  }),
});

const bestof = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/bestof' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.date(),
    author: z.string().default('AI Tools Team'),
    category: z.string().default('bestof'),
    tools: z.array(z.object({
      name: z.string(),
      description: z.string(),
      rating: z.number().min(1).max(5),
      highlight: z.string().optional(),
    })),
    image: z.string().optional(),
    featured: z.boolean().default(false),
    tags: z.array(z.string()).default([]),
  }),
});

export const collections = { reviews, comparisons, alternatives, bestof };
