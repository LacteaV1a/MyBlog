from django.template.defaultfilters import slugify
from taggit.models import Tag, TaggedItem


alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}

class RuTag(Tag):
  class Meta:
    proxy = True

  def slugify(self, tag, i=None):
    return slugify(''.join(alphabet.get(w, w) for w in tag.lower()))

class RuTaggedItem(TaggedItem):
  class Meta:
    proxy = True

  @classmethod
  def tag_model(cls):
    return RuTag