import random
import logging

loggers = logging.getLogger(__name__)

class Action:
    """
    Action class to define the types of actions that can be performed on a sentence.
    
    SUBSTITUTE: words are substituted randomly
    DELETE: words are removed randomly
    SWAP: adjacent words swapped randomly
    CROP: set of continuous words removed randomly
    """
    SUBSTITUTE = 'substitute'
    DELETE = 'delete'
    SWAP = 'swap'
    CROP = 'crop'

class RandomAugmenter():
    def __init__(self):
        loggers.info("RandomAugmenter initialized")
        
    def __call__(self, data, action, aug_percent=0.3, aug_min=1, aug_max=10, skipwords=None, target_words=None):
        """
        Random text augmentation function.
        
        :param data: Input text to augment.
        :param action: Action to perform ('substitute', 'delete', 'swap', or 'crop').
        :param aug_percent: Percentage of words to augment.
        :param aug_min: Minimum number of words to augment.
        :param aug_max: Maximum number of words to augment.
        :param skipwords: List of words to skip during augmentation.
        :param target_words: List of words for replacement (only for 'substitute' action).
        :return: Augmented text.
        """
        if not data or not data.strip():
            return data
        original_sentence = data
        words = data.split()
        # calculate count of augmentation
        self.aug_count = max(aug_min, int(len(words) * aug_percent))
        self.aug_count = min(self.aug_count, aug_max, len(words))
        self.target_words = target_words or ['_']
        self.skipwords = skipwords
        
        if action == Action.SUBSTITUTE:
            words = self.substitute(words)
        elif action == Action.DELETE:
            words = self.delete(words)
        elif action == Action.SWAP:
            words = self.swap(words)
        elif action == Action.CROP:
            words = self.crop(words)
        
        augmented_words = ' '.join(words)
        return original_sentence, augmented_words
    
    # https://arxiv.org/pdf/1703.02573.pdf, https://arxiv.org/pdf/1712.06751.pdf, https://arxiv.org/pdf/1806.09030.pdf
    # https://arxiv.org/pdf/1905.11268.pdf,
    def substitute(self,words):
        """
        Substitute selected words with random target words.
        """
        change_seq = 0  # Track sequence of changes
        aug_indices = random.sample(range(len(words)), self.aug_count)  # Randomly select indices to augment
        aug_indices.sort(reverse=True)  # Process from the end to avoid index shifts

        for idx in aug_indices:
            original_token = words[idx]  # Original word at this position
            # Skip if the word is in the self.skipwords list
            if self.skipwords and original_token in self.skipwords:
                continue
            new_token = random.choice(self.target_words)  # Choose a replacement word from target_words
            # Apply capitalization of the original token to the new token if necessary
            if idx == 0:
                new_token = original_token[0].upper() + new_token[1:] if original_token[0].isupper() else new_token
            change_seq += 1  # Increment change sequence
            words[idx] = new_token  # Replace the word

        return words

    # https://arxiv.org/pdf/1905.11268.pdf, https://arxiv.org/pdf/1809.02079.pdf, https://arxiv.org/pdf/1903.09460.pdf
    def delete(self,words):
        aug_indices = sorted(random.sample(range(len(words)), self.aug_count), reverse=True)
        for idx in aug_indices:
            if self.skipwords and words[idx] in self.skipwords:
                continue
            words.pop(idx)
        return words

    # https://arxiv.org/pdf/1711.02173.pdf, https://arxiv.org/pdf/1809.02079.pdf, https://arxiv.org/pdf/1903.09460.pdf
    def swap(self,words):
        """
        Swap selected words with adjacent words.
        """
        change_seq = 0  # Track sequence of changes
        aug_indices = random.sample(range(len(words) - 1), self.aug_count)  # Randomly select indices to augment
        aug_indices.sort(reverse=True)  # Process from the end to avoid index shifts

        for idx in aug_indices:
            # Ensure swapping does not include self.skipwords
            if self.skipwords and (words[idx] in self.skipwords or words[idx + 1] in self.skipwords):
                continue
            
            # Swap the word with its adjacent word
            original_token = words[idx]
            swap_token = words[idx + 1]
            
            # Check if the word is at the beginning, and maintain proper case if necessary
            if idx == 0:
                # Capitalize swap token if needed
                swap_token = original_token[0].upper() + swap_token[1:] if original_token[0].isupper() else swap_token
                original_token = original_token.lower() if original_token[0].isupper() else original_token

            # Perform swap
            words[idx], words[idx + 1] = swap_token, original_token
            change_seq += 1  # Increment change sequence

        return words

    def crop(self,words):
        if len(words) < 2:
            return words  # Skip if not enough words to crop
        start_idx = random.randint(0, len(words) - self.aug_count)
        end_idx = start_idx + self.aug_count
        return words[:start_idx] + words[end_idx:]