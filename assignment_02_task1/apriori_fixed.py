from itertools import chain, combinations, filterfalse
import line_profiler

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

def join_set(itemsets, k):
    return set(
        [itemset1.union(itemset2) for itemset1 in itemsets for itemset2 in itemsets if len(itemset1.union(itemset2)) == k]
    )

def itemsets_support(transactions, itemsets, min_support):
    support_count = {itemset: 0 for itemset in itemsets}
    for transaction in transactions:
        for itemset in itemsets:
            if itemset.issubset(transaction):
                support_count[itemset] += 1
    n_transactions = len(transactions)
    return {itemset: support / n_transactions for itemset, support in support_count.items() if support / n_transactions >= min_support}

def apriori_fixed(transactions, min_support):
    items = set(chain(*transactions))
    itemsets = [frozenset([item]) for item in items]
    itemsets_by_length = [set()]
    k = 1
    while itemsets:
        support_count = itemsets_support(transactions, itemsets, min_support)

        # NEW:
        if not support_count:
            break
        # END NEW

        itemsets_by_length.append(set(support_count.keys()))
        k += 1

        # OLD:
        # itemsets = join_set(itemsets, k)
        # NEW:
        itemsets = join_set(support_count.keys(), k)
        # END NEW

    frequent_itemsets = set(chain(*itemsets_by_length))
    return frequent_itemsets, itemsets_by_length

def association_rules_fixed(transactions, min_support, min_confidence):
    frequent_itemsets, itemsets_by_length = apriori_fixed(transactions, min_support)
    rules = []
    for itemset in frequent_itemsets:
        for subset in filterfalse(lambda x: not x, powerset(itemset)):
            antecedent = frozenset(subset)
            consequent = itemset - antecedent
            support_antecedent = len([t for t in transactions if antecedent.issubset(t)]) / len(transactions)
            support_itemset = len([t for t in transactions if itemset.issubset(t)]) / len(transactions)
            
            # NEW:
            support_consequent = len([t for t in transactions if consequent.issubset(t)]) / len(transactions)
            lift = support_itemset / (support_antecedent * support_consequent)
            # END NEW

            # OLD:
            # confidence = support_itemset / support_antecedent
            # NEW:
            confidence = support_itemset / support_antecedent if consequent else support_antecedent
            # END NEW

            if confidence >= min_confidence and consequent:
                # OLD:
                # rules.append((antecedent, consequent, support_itemset, confidence))
                # NEW:
                rules.append((antecedent, consequent, support_itemset, confidence, lift))
                # END NEW
    return rules

# Example usage
transactions = [
    {"beer", "wine", "cheese"},
    {"beer", "potato chips"},
    {"eggs", "flour", "butter", "cheese"},
    {"eggs", "flour", "butter", "beer", "potato chips"},
    {"wine", "cheese"},
    {"potato chips"},
    {"eggs", "flour", "butter", "wine", "cheese"},
    {"eggs", "flour", "butter", "beer", "potato chips"},
    {"wine", "beer"},
    {"beer", "potato chips"},
    {"butter", "eggs"},
    {"beer", "potato chips"},
    {"flour", "eggs"},
    {"beer", "potato chips"},
    {"eggs", "flour", "butter", "wine", "cheese"},
    {"beer", "wine", "potato chips", "cheese"},
    {"wine", "cheese"},
    {"beer", "potato chips"},
    {"wine", "cheese"},
    {"beer", "potato chips"}
]

min_support = 0.4
min_confidence = 0.5

def main():
    rules = association_rules_fixed(transactions, min_support, min_confidence)
    for antecedent, consequent, support, confidence, lift in rules:
        print(f"{antecedent} => {consequent} (support={support:.3f}, confidence={confidence:.3f}, lift={lift:.3f})")

if __name__ == "__main__":
    main()