"""
Create synthetic justice support samples
Target: Reduce 0→1 errors for justice-related comments
"""
import pandas as pd
from datetime import datetime

print("="*80)
print("⚖️ CREATING JUSTICE SUPPORT SAMPLES")
print("="*80)

# Templates for justice support (Label 0 - neutral/positive)
justice_templates = [
    # Pháp luật xử lý
    ("tin tức pháp luật", "pháp luật sẽ xử lý nghiêm minh"),
    ("vụ án mới nhất", "mong pháp luật xử lý đúng người đúng tội"),
    ("cập nhật vụ việc", "tin tưởng pháp luật sẽ làm rõ"),
    ("phân tích vụ án", "pháp luật cần can thiệp ngay"),
    ("bình luận thời sự", "ủng hộ pháp luật xử lý nghiêm"),
    
    # Bắt đi tù
    ("kẻ gian bị bắt", "bắt đi tù là đúng rồi"),
    ("tội phạm sa lưới", "bắt được rồi phải xử nghiêm"),
    ("cảnh sát triệt phá", "bắt hết bọn này đi"),
    ("vụ bắt giữ", "bắt đúng người rồi"),
    ("tin pháp luật", "bắt kịp thời quá"),
    
    # Phạt nặng
    ("vi phạm giao thông", "phạt nặng để răn đe"),
    ("xử phạt hành chính", "phạt đúng rồi không oan"),
    ("mức phạt mới", "phạt nặng là cần thiết"),
    ("quy định phạt", "phạt như vậy là hợp lý"),
    ("cảnh báo phạt", "phạt để mọi người biết sợ"),
    
    # Tù giam
    ("tuyên án", "tù 10 năm là xứng đáng"),
    ("kết quả xét xử", "vào tù là đúng rồi"),
    ("bản án", "giam đi cho xã hội thanh bình"),
    ("phiên tòa", "tù chung thân cũng không oan"),
    ("thi hành án", "vào tù xong sẽ biết ăn năn"),
    
    # Xử lý nghiêm
    ("yêu cầu xử lý", "xử lý nghiêm minh đi"),
    ("kiến nghị", "cần xử lý ngay"),
    ("đề xuất", "xử lý theo pháp luật"),
    ("phản ánh", "mong được xử lý sớm"),
    ("báo cáo", "xử lý đúng quy định"),
    
    # Trừng phạt
    ("kêu gọi công lý", "trừng phạt kẻ xấu"),
    ("đòi công bằng", "trừng trị nghiêm khắc"),
    ("yêu cầu công lý", "trừng phạt đúng người"),
    ("ủng hộ công lý", "trừng phạt để răn đe"),
    ("tin tưởng công lý", "trừng trị theo luật"),
    
    # Mixed với context tích cực
    ("vụ bắt tội phạm", "cảnh sát làm tốt lắm bắt được bọn này"),
    ("tin vui pháp luật", "cuối cùng cũng bắt được rồi"),
    ("công lý được thực thi", "phạt đúng người rồi"),
    ("xã hội an toàn hơn", "bắt hết bọn xấu đi"),
    ("niềm tin pháp luật", "tin tưởng luật pháp xử lý công bằng"),
    
    # Context với đại từ nhưng không toxic
    ("bình luận vụ việc", "bắt nó đi là đúng rồi"),
    ("ý kiến cá nhân", "phạt nó nặng đi"),
    ("quan điểm", "cho nó vào tù xứng đáng"),
    ("nhận xét", "xử lý nó theo luật"),
    ("đánh giá", "trừng phạt nó nghiêm khắc"),
    
    # Real-world scenarios
    ("tai nạn giao thông", "tài xế say rượu phải bắt đi tù"),
    ("vụ trộm cắp", "bắt được rồi phạt nặng đi"),
    ("lừa đảo online", "mong pháp luật xử lý sớm"),
    ("bạo hành gia đình", "phải bắt giam người này"),
    ("tham nhũng", "xử lý nghiêm minh theo luật"),
    
    # With emotion but still neutral
    ("phẫn nộ với tội ác", "phải trừng trị nghiêm khắc"),
    ("bức xúc với kẻ xấu", "bắt đi tù ngay"),
    ("căm phẫn tội phạm", "phạt thật nặng"),
    ("tức giận với hành vi", "xử lý theo pháp luật"),
    ("không chấp nhận được", "giam đi cho xã hội yên"),
]

# Create samples
samples = []
for title, comment in justice_templates:
    training_text = f"{title} </s> {comment}"
    samples.append({
        'training_text': training_text,
        'text_raw': training_text,
        'label': 0,  # Neutral - justice support
        'note': 'Justice support - synthetic',
        'source_file': 'create_justice_samples',
        'labeler': 'synthetic',
        'has_teencode': False,
        'confidence': 'HIGH',
        'sampling_strategy': 'justice_support_synthetic',
        'raw_comment': comment,
        'raw_title': title
    })

# Add some variations
print(f"\n📊 Creating variations...")
variations = []
for sample in samples[:20]:  # Take first 20 and create variations
    text = sample['training_text']
    
    # Variation 1: Add positive emotion
    var1 = text.replace('</s>', '</s> mình ủng hộ')
    variations.append({**sample, 'training_text': var1, 'text_raw': var1})
    
    # Variation 2: Add agreement
    var2 = text.replace('</s>', '</s> đúng rồi')
    variations.append({**sample, 'training_text': var2, 'text_raw': var2})

samples.extend(variations)

# Create DataFrame
df = pd.DataFrame(samples)

print(f"\n📊 TOTAL CREATED: {len(df)} samples")
print(f"   Label 0: {len(df[df['label'] == 0])}")

# Save
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = f'AUGMENTED_JUSTICE_SUPPORT_{timestamp}.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n💾 Saved: {output_file}")

# Also save Excel for review
excel_file = f'AUGMENTED_JUSTICE_SUPPORT_{timestamp}.xlsx'
df.to_excel(excel_file, index=False)
print(f"💾 Saved: {excel_file}")

# Show samples
print(f"\n📋 SAMPLE EXAMPLES:")
print("-" * 80)
for i, row in df.head(10).iterrows():
    print(f"{i+1}. {row['training_text']}")

print("\n" + "="*80)
print("✅ CREATION COMPLETE!")
print("="*80)
print(f"\n📋 NEXT STEPS:")
print(f"   1. Review: {excel_file}")
print(f"   2. If OK, merge with training data:")
print(f"      python merge_augmented_data.py")
