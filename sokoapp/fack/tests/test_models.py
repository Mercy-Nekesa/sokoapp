from __future__ import absolute_import

import datetime
import django.test
from django.core.urlresolvers import reverse
from ..models import Topic, Question

class FAQModelTests(django.test.TestCase):
    
    def test_model_save(self):
        t = Topic.objects.create(name='t', slug='t')
        q = Question.objects.create(
            text = "What is your quest?",
            answer = "I see the grail!",
            topic = t
        )
        self.assertEqual(q.created_on.date(), datetime.date.today())
        self.assertEqual(q.updated_on.date(), datetime.date.today())
        self.assertEqual(q.slug, "what-is-your-quest")
        
    def test_model_save_duplicate_slugs(self):
        t = Topic.objects.create(name='t', slug='t')
        q = Question.objects.create(
            text = "What is your quest?",
            answer = "I see the grail!",
            topic = t
        )
        q2 = Question.objects.create(
            text = "What is your quest?",
            answer = "I see the grail!",
            topic = t
        )
        self.assertEqual(q2.slug, 'what-is-your-quest-1')

    def test_permalinks(self):
        # Perhaps a bit overkill to test, but we missed it initially
        t = Topic.objects.create(name='t', slug='t')
        q = Question.objects.create(
            text = "What is your quest?",
            answer = "I see the grail!",
            topic = t
        )
        t_url = t.get_absolute_url()
        t_test_url = reverse('faq_topic_detail', args=[t.slug])
        q_url = q.get_absolute_url()
        q_test_url = reverse('faq_question_detail', args=[t.slug, q.slug])

        self.assertEqual(t_url, t_test_url)
        self.assertEqual(q_url, q_test_url)

