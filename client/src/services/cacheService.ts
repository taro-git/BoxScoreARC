type RemovalPolicy = 'farthest' | 'oldest' | 'none' | 'lru'

// eslint-disable-next-line @typescript-eslint/no-unused-vars
interface CommonCacheOptions<T> {
  maxItems?: number
  baseKey?: number
  ttlSeconds?: number
  cacheFilter?: (key: number, value: unknown) => boolean
}

interface FarthestCacheOptions<T> extends CommonCacheOptions<T> {
  removalPolicy: 'farthest'
  getDistanceForFarthest: (key: number, value: T) => number
}

interface OtherCacheOptions<T> extends CommonCacheOptions<T> {
  removalPolicy?: 'oldest' | 'none' | 'lru'
  getDistanceForFarthest?: never
}

type CacheOptions<T> = FarthestCacheOptions<T> | OtherCacheOptions<T>


interface CacheEntry<T> {
  value: T
  timestamp: number
  lastAccessed: number
}

// MYTODO データベースを活用したキャッシュの検討
export class CacheService<T> {
  private cache = new Map<number, CacheEntry<T>>()
  private maxItems: number
  private removalPolicy: RemovalPolicy
  private ttlSeconds?: number
  private getDistanceForFarthest: (key: number, value: T) => number
  private cacheFilter?: (key: number, value: unknown) => boolean

  constructor(options: CacheOptions<T> = {}) {
    this.maxItems = options.maxItems ?? 100
    this.removalPolicy = options.removalPolicy ?? 'lru'
    this.ttlSeconds = options.ttlSeconds
    this.getDistanceForFarthest = options.getDistanceForFarthest ?? (() => {
      throw new Error('getDistanceForFarthest was called, but no implementation was provided.')
    })
    this.cacheFilter = options.cacheFilter
  }

  async getOrFetch(key: number, fetcher: () => Promise<T>): Promise<T> {
    const now = Date.now()
    const cached = this.cache.get(key)

    if (cached) {
      if (this.ttlSeconds !== undefined) {
        const age = (now - cached.timestamp) / 1000
        if (age > this.ttlSeconds) {
          this.cache.delete(key)
        } else {
          cached.lastAccessed = now
          return cached.value
        }
      } else {
        cached.lastAccessed = now
        return cached.value
      }
    }

    const value = await fetcher()
    if (this.cacheFilter === undefined || (this.cacheFilter && this.cacheFilter(key, value))){
      this.cache.set(key, {
        value,
        timestamp: now,
        lastAccessed: now,
      })
    }

    if (this.cache.size > this.maxItems) {
      this.removeOne()
    }

    return value
  }

  private removeOne() {
    if (this.removalPolicy === 'none') return

    let removeTargetKey: number | null = null
    let highestRemovalPriority = 0

    for (const [key, entry] of this.cache.entries()) {
      let removalPriority = 0
      switch (this.removalPolicy) {
        case 'farthest':
          removalPriority = this.getDistanceForFarthest(key, entry.value)
          break
        case 'oldest':
          removalPriority = Date.now() - entry.timestamp
          break
        case 'lru':
          removalPriority = Date.now() - entry.lastAccessed
          break
      }

      if (removalPriority > highestRemovalPriority) {
        highestRemovalPriority = removalPriority
        removeTargetKey = key
      }
    }

    if (removeTargetKey !== null) {
        this.cache.delete(removeTargetKey)
    }
  }

  clear() {
    this.cache.clear()
  }

  size(): number {
    return this.cache.size
  }
}
