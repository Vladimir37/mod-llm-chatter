#ifndef MOD_LLM_CHATTER_REACTIVITY_H
#define MOD_LLM_CHATTER_REACTIVITY_H

/*
 * mod-llm-chatter - world reactivity
 *
 * Owns the live side of letters and rumors: records what a real
 * player did in llm_reactivity_inbox, and sends the letters the
 * bridge has written. The bridge owns every decision about what
 * a deed means and every word that is said about it.
 */

class Player;

void AddLLMChatterReactivityScripts();
void DeliverPendingReactivityLetters();

// True when the bridge has a rumor about this player that is
// still fresh and may be told in the player's current zone.
bool HasFreshRumorHere(Player* player);

#endif
